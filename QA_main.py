# -*- coding:utf-8 -*-
''' 根据问题，获得答案，返回数据到web_server.py '''

from answer_search import *
from question_classification import *
from question_parser import *


class QuestionAnswerSystem(object):
	def __init__(self):
		self.classifier = QuestionClassifier()
		self.question_parser = QuestionParser()
		self.answer_searcher = AnswerSearcher()

	def question_answer_main(self, question):
		res = {}
		res['entry_rc'] = []
		res['entry_cn'] = []
		res['entry_tr'] = []
		res['data_list'] = []
		res['answer'] = "非常抱歉，暂时未找到答案，试试其它的问题呢"
		classify_res = self.classifier.classify_main(question)
		if not classify_res:
			return res

		res_sql = self.question_parser.parser_main(classify_res)
		final_answers = self.answer_searcher.search_main(res_sql)
		rc = ''
		for i, j in classify_res['keywords'].items():
			rc = rc + ''.join(i) + '---' + ''.join(j) + '\n'
		res['entry_rc'] = rc
		res['entry_cn'] = ' ;'.join(classify_res['question_types'])
		res['entry_tr'] = classify_res['triples']
		if final_answers:
			res['answer'] = '\n'.join(final_answers['final_answers'])
			res['data_list'] = final_answers['data_list']
		return res
