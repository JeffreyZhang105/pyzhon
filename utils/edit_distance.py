# -*- coding: utf-8 -*-


def get_similarity(text_x, text_y):
	""" Gets similarity of two strings.

	:param text_x: One string
	:param text_y: The other string
	:return: Similarity of two strings represented by floating point number. e.g. "0.8"
	"""
	distance = get_edit_distance(text_x, text_y)
	similarity = 1 - distance / max(len(text_x), len(text_y))
	return similarity


def get_edit_distance(text_x, text_y):
	""" Gets similarity of two strings.

	:param text_x: One string
	:param text_y: The other string
	:return: Edit distance between strings by integer.
	"""
	len_x, len_y = len(text_x), len(text_y)
	matrix = [
		[idx_x if idx_y == 0 else idx_y if idx_x == 0 else None for idx_x in range(len_x + 1)]
		for idx_y in range(len_y + 1)
	]

	for idx_x in range(1, len_x + 1):
		for idx_y in range(1, len_y + 1):
			setp_max = min(
				matrix[idx_y - 1][idx_x] + 1,
				matrix[idx_y][idx_x - 1] + 1,
				matrix[idx_y - 1][idx_x - 1] + (0 if text_x[idx_x - 1] == text_y[idx_y - 1] else 1)
			)
			matrix[idx_y][idx_x] = setp_max

	return matrix[len_y][len_x]
