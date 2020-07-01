import numpy as np
from keras.models import load_model
from pre_process import norm_img

SIZE_NOPADD = 20


def prediction(crops_img):
	arr = []
	model = load_model('model.h5')
	for val in crops_img:
		prediction = model.predict(val.reshape(1, 28, 28, 1))
		max = np.argmax(prediction)
		if max == 10:
			max = '+'
		elif max == 11:
			max = '-'
		elif max == 12:
			max = '*'
		elif max == 13:
			max = '/'
		arr.append(max)
	return arr


# crops_img = norm_img('so.JPG', 20)
# predict = prediction(crops_img)


# xoá khoảng trống của 1 số
def remove_space(array):
	arr_new = []
	str_n = ''
	for val in array:
		if val != '+' and val != '-' and val != '*' and val != '/':
			str_n += str(val)
		else:
			if len(str_n) >= 1:
				arr_new.append(str_n)
				str_n = ''
			arr_new.append(val)
	if len(str_n) >= 1:
		arr_new.append(str_n)
	return arr_new

def display_prediction(url):
	crops_imgs = norm_img(url, SIZE_NOPADD)
	predict = prediction(crops_imgs)
	ex = remove_space(predict)
	return ' '.join(ex)
# print(display_prediction('D:/python/project 4/app/static/demo/demo2.jpg'))
# arr = remove_space(arr)
# độ ưu tiên
def do_uu_tien(val):
	if val == '(':
		return 0
	if val == '+' or val == '-':
		return 1
	if val == '*' or val == '/':
		return 2
	return 3


# kiểm tra là số
def isDigit(num):
	try:
		ex = int(num)
		return True
	except:
		return False


# ex = remove_space(predict)


# print(ex)

# convert to postfix
def toPostfix(expression):
	stack = []
	postfix = []
	for val in expression:
		if isDigit(val):
			postfix.append(val)
		else:
			if len(stack) == 0 or val == '(' or do_uu_tien(stack[-1]) < do_uu_tien(val):
				stack.append(val)
			elif do_uu_tien(val) <= do_uu_tien(stack[-1]):
				postfix.append(stack.pop(-1))
				stack.append(val)
	if len(stack) >= 1:
		postfix += stack[::-1]
	return postfix


# elif val == ')':
# 	id = stack[::-1].index(')')

# ex = toPostfix(ex)


# compute value postfix
def compute_value_postfix(ex_postfix):
	stack = []
	result = 0
	for value in ex_postfix:
		if isDigit(value):
			stack.append(int(value))
		else:
			if value == '*':
				result = stack.pop(-1) * stack.pop(-1)
			elif value == '/':
				result = stack.pop(-1) / stack.pop(-1)
			elif value == '+':
				result = stack.pop(-1) + stack.pop(-1)
			else:
				ele_2 = stack.pop(-1)
				ele_1 = stack.pop(-1)
				result = ele_1 - ele_2
			stack.append(result)
	return result


def compute(url):
	crops_imgs = norm_img(url, SIZE_NOPADD)
	predict = prediction(crops_imgs)
	remove_space_img = remove_space(predict)
	post_fix = toPostfix(remove_space_img)
	return compute_value_postfix(post_fix)

#
# print(compute_value_postfix(['3', '10', '-', '9', '4', '*', '+']))
