from Container import ThreadContainerLock
from traceback import format_exc
import concurrent.futures
from pathlib import Path
import cv2
import os


def removeBackWhiteBackground(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to identify white pixels
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    # Apply the mask to remove the white background
    result = cv2.bitwise_and(image, image, mask=mask)

    return result


def matchImageWorker(
    container: ThreadContainerLock, targetImage, targetWidth: int, targetHeight: int
):
    try:
        currentImagePath = container.GetNext()
        if currentImagePath.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            currentImage = cv2.imread(currentImagePath)
            currentImage = cv2.resize(currentImage, (targetWidth, targetHeight))
            currentImage = removeBackWhiteBackground(currentImage)
            result = cv2.matchTemplate(currentImage, targetImage, cv2.TM_CCOEFF_NORMED)
            _, similarity, _, _ = cv2.minMaxLoc(result)
        return currentImagePath, similarity
    except:
        print(f"ERROR ON IMAGE : {currentImagePath}" + format_exc())
        return currentImagePath,-100

def matchImage(folderPath, targetImagePath, threadCount: int):
    targetImage = cv2.imread(targetImagePath)
    targetImage = removeBackWhiteBackground(targetImage)
    targetHeight, targetWidth = targetImage.shape[:2]
    bestMatchPath = None
    bestSimilarity = 0.0
    filePathsContainer = ThreadContainerLock(
        [str(Path(folderPath) / path) for path in os.listdir(folderPath)]
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=threadCount) as executor:
        futures = [
            executor.submit(
                matchImageWorker,
                filePathsContainer,
                targetImage,
                targetWidth,
                targetHeight,
            )
            for filename in os.listdir(folderPath)
        ]
        concurrent.futures.wait(futures)
        for future in futures:
            current_match_path, similarity = future.result()
            if similarity > bestSimilarity:
                bestSimilarity = similarity
                bestMatchPath = current_match_path

    if bestMatchPath:
        return bestMatchPath.split("/")[-1].split("\\")[-1].split(".")[0]
    else:
        return None
