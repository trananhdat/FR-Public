import cv2

def draw_fancy_box(img, pt1, pt2, color, thickness, d):
    '''
    To draw some fancy box around founded faces in stream
    '''
    x1, y1 = pt1
    x2, y2 = pt2

    # Top left
    cv2.line(img, (x1, y1), (x1+ d, y1), color, thickness)
    cv2.line(img, (x1, y1), (x1, y1+ d), color, thickness)
    # cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)

    # Top right
    cv2.line(img, (x2, y1), (x2- d, y1), color, thickness)
    cv2.line(img, (x2, y1), (x2, y1+ d), color, thickness)
    # cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)

    # Bottom left
    cv2.line(img, (x1, y2), (x1+ d, y2), color, thickness)
    cv2.line(img, (x1, y2), (x1, y2- d), color, thickness)
    # cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)

    # Bottom right
    cv2.line(img, (x2, y2), (x2- d, y2), color, thickness)
    cv2.line(img, (x2, y2), (x2, y2 - d), color, thickness)
    # cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)

def in_frame(x1,y1, x2,y2, h, w):

    """
    Kiểm tra khuôn mặt đang tracking có đang nằm trong khung hình không
    """
    # print(h, w)
    if x1 <= 5 or x1 >= w - 5:
        # print('x1 = {}'.format(x1))
        
        return False 
    if x2 <= 5 or x2 >= w - 5:
        # print('x2 = {}'.format(x2))
        return False

    if y1 <= 5 or y1 >= h - 5:
        # print('y1 = {}'.format(y1))
        return False

    if y2 <= 5 or y2 >= h - 5:
        # print('y2 = {}'.format(y2))
        return False

    return True