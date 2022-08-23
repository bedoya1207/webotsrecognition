import cv2

def analizar(imagen:str,fondo:str ):
    # read the images
    img1 = cv2.imread(imagen)  
    img2 = cv2.imread(fondo)

    img2 = cv2.flip(img2,1)
    img2 = cv2.rotate(img2,cv2.ROTATE_90_COUNTERCLOCKWISE)
    #create SIFT detector
    sift = cv2.SIFT_create()
    # detect SIFT features in both images
    keypoints_1, descriptors_1 = sift.detectAndCompute(img1,None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(img2,None)
    # create feature matcher
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
    # match descriptors of both images
    matches = bf.match(descriptors_1,descriptors_2)
    # sort matches by distance
    matches = sorted(matches, key = lambda x:x.distance)
    # draw first 50 matches
    matched_img = cv2.drawMatches(img1, keypoints_1, img2, keypoints_2, matches, img2, flags=2)
    # save the image
    cv2.imwrite("matches %s.png" %imagen, matched_img)
    # send num of matches
    return len(matches)