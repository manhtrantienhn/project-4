import numpy as np
import cv2

def crop_image(x1, y1, x2, y2, img):
  if np.ndim(img) == 3:
    crop = img[y1:y2, x1:x2, :]
  else:
    crop = img[y1:y2, x1:x2]
  return crop

# remove khung chồng lấn
def non_max_suppression(boxes, overlapThresh):
  '''
  boxes: List các bounding box
  overlapThresh: Ngưỡng overlapping giữa các hình ảnh
  '''
  # Nếu không có bounding boxes thì trả về empty list
  if len(boxes)==0:
    return []
  # Nếu bounding boxes nguyên thì chuyển sang float.
  if boxes.dtype.kind == "i":
    boxes = boxes.astype("float")

  # Khởi tạo list của index được lựa chọn
  pick = []

  # Lấy ra tọa độ của các bounding boxes
  x1 = boxes[:,0]
  y1 = boxes[:,1]
  x2 = boxes[:,2]
  y2 = boxes[:,3]

  # Tính toàn diện tích của các bounding boxes và sắp xếp chúng theo thứ tự từ bottom-right, chính là tọa độ theo y của bounding box
  area = (x2 - x1 + 1) * (y2 - y1 + 1)
  idxs = np.argsort(y2)
  # Khởi tạo một vòng while loop qua các index xuất hiện trong indexes
  while len(idxs) > 0:
    # Lấy ra index cuối cùng của list các indexes và thêm giá trị index vào danh sách các indexes được lựa chọn
    last = len(idxs) - 1
    i = idxs[last]
    pick.append(i)

    # Tìm cặp tọa độ lớn nhất (x, y) là điểm bắt đầu của bounding box và tọa độ nhỏ nhất (x, y) là điểm kết thúc của bounding box
    xx1 = np.maximum(x1[i], x1[idxs[:last]])
    yy1 = np.maximum(y1[i], y1[idxs[:last]])
    xx2 = np.minimum(x2[i], x2[idxs[:last]])
    yy2 = np.minimum(y2[i], y2[idxs[:last]])

    # Tính toán width và height của bounding box
    w = np.maximum(0, xx2 - xx1 + 1)
    h = np.maximum(0, yy2 - yy1 + 1)

    # Tính toán tỷ lệ diện tích overlap
    overlap = (w * h) / area[idxs[:last]]

    # Xóa index cuối cùng và index của bounding box mà tỷ lệ diện tích overlap > overlapThreshold
    idxs = np.delete(idxs, np.concatenate(([last],
      np.where(overlap > overlapThresh)[0])))
  # Trả ra list các index được lựa chọn
  return boxes[pick].astype("int")

def sort_img(ele):
    return ele[0]


def img_preprocessing(url):
  img = cv2.imread(url)
  grey = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
  # Chuyển sang ảnh nhị phân
  _, thresh = cv2.threshold(grey, 100, 255, cv2.THRESH_BINARY)
  #tìm contour trên ảnh nhị phân
  contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  #tìm diện tích toàn bộ các contours
  area_cnt = [cv2.contourArea(cnt) for cnt in contours]

  boundingBoxes = []
  for i in range(len(area_cnt)):
    cnt = contours[i]
    x,y,w,h = cv2.boundingRect(cnt)
    x1, y1, x2, y2 = x, y, x+w, y+h
    boundingBoxes.append((x1, y1, x2, y2))
  # boundingBoxes.sort(key=sort_img)

  # Remove đi bounding box parent (chính là khung hình bound toàn bộ hình ảnh), nếu không khi áp dụng non max suppression chỉ giữ lại bounding box này
  boundingBoxes = [box for box in boundingBoxes if box[:2] != (0, 0)]
  boundingBoxes = np.array(boundingBoxes)
  pick = non_max_suppression(boundingBoxes, 0.5)
  arr = []
  for i in pick:
    i = tuple(i)
    arr.append(i)
  pick =[]
  arr.sort(key=sort_img)
  for j in arr:
    pick.append(list(j))
  #crop
  crop_images = [crop_image(x1, y1, x2, y2, img) for (x1, y1, x2, y2) in pick]
  return crop_images

def resize_img(img, size_no_pad):
  grey = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
  ret, thresh = cv2.threshold(grey.copy(), 100, 255, cv2.THRESH_BINARY_INV)
  #compute high, width of image
  high, width = img.shape[0], img.shape[1]
  #resize image
  h, w = (size_no_pad, width*size_no_pad // high) if high > width else (high*size_no_pad // width, size_no_pad)
  resized_digit = cv2.resize(thresh, (w, h))
  #compute padded for h,w
  pad_h = (28-h)//2
  pad_w = (28-w)//2
  #add padded to h,w -> (28,28)
  padded_digit = np.pad(resized_digit, ((pad_h, pad_h),(pad_w, pad_w)), "constant", constant_values=0)
  if padded_digit.shape[0]!=28:
    padded_digit = np.pad(padded_digit, ((1, 0),(0, 0)), "constant", constant_values=0)
  elif padded_digit.shape[1]!=28:
    padded_digit = np.pad(padded_digit, ((0, 0),(1, 0)), "constant", constant_values=0)
  return padded_digit

# chuẩn hóa ảnh đã crop
def norm_img(url, size_nopadd):
	crops = []
	cr = img_preprocessing(url)
	for val in cr:
		crops.append(resize_img(val, size_no_pad = size_nopadd))
	return crops

# url = '1.jpg'
# crops = norm_img(url, 20)
# fig, ax = plt.subplots(nrows =1,ncols=6,figsize=(12,4))
# fig.suptitle('crop')
# for i in range(6):
#   try:
#     ax[i].imshow(crops[i], cmap='gray')
#     ax[i].set_xlabel('Sub Image '+str(i))
#   except:
#     next
#
# plt.show()
#
