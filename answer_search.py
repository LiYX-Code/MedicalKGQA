# -*- coding:utf-8 -*-
''' 获取答案 '''

from py2neo import Graph


class AnswerSearcher(object):
	def __init__(self):
		self.g = Graph(
			host="127.0.0.1",
			http_port=7474,
			user="neo4j",
			password="410221ABC")
		self.num_limit = 20

	def search_main(self, sql_list):
		res = {}
		final_answers = []
		data_list = []
		for sql_dict in sql_list:
			question_type = sql_dict['question_type']
			queries = sql_dict['sql']
			answers = []
			for query in queries:
				ress = self.g.run(query).data()
				answers += ress
			st = self.answer_prettify(question_type, answers)
			if st:
				final_answers.append(st['final_answer'])
				data_list.append(st['data_list'])
		res['final_answers'] = final_answers
		res['data_list'] = data_list
		return res

	''' 根据问题的类型，进行相应的回复 '''
	def answer_prettify(self, question_type, answers):
		res = {}
		final_answer = []
		data_list = []
		if not answers:
			return ''
		if question_type == 'disease_symptom':
			desc = [i['n.name'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
			data_list = [subject, '症状', '；'.join(list(set(desc))[:self.num_limit])]

		elif question_type == 'symptom_disease':
			desc = [i['m.name'] for i in answers]
			subject = answers[0]['n.name']
			final_answer = '症状{0}可能染上的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
			data_list = [subject, '相关疾病', '；'.join(list(set(desc))[:self.num_limit])]

		elif question_type == 'disease_cause':
			desc = [i['m.cause'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}可能的成因有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
			data_list = [subject, '成因', '；'.join(list(set(desc))[:self.num_limit])]

		elif question_type == 'disease_prevent':
			desc = [i['m.prevent'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}的预防措施包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
			data_list = [subject, '预防措施', '；'.join(list(set(desc))[:self.num_limit])]

		elif question_type == 'disease_treat_cycle':
			desc = [i['m.treat_cycle'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}治疗可能持续的周期为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
			data_list = [subject, '持续周期', '；'.join(list(set(desc))[:self.num_limit])]

		elif question_type == 'disease_treat_way':
			desc = [';'.join(i['m.treat_way']) for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}可以尝试如下治疗：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
			data_list = [subject, '治疗方法', '；'.join(list(set(desc))[:self.num_limit])]

		elif question_type == 'disease_cure_prob':
			desc = [i['m.cure_prob'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}治愈的概率为（仅供参考）：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
			data_list = [subject, '治愈概率', '；'.join(list(set(desc))[:self.num_limit])]

		elif question_type == 'disease_susceptible_people':
			desc = [i['m.susceptible_people'] for i in answers]
			subject = answers[0]['m.name']

			final_answer = '{0}的易感人群包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
			data_list = [subject, '易感人群', '；'.join(list(set(desc))[:self.num_limit])]

		elif question_type == 'disease_desc':
			desc = [i['m.desc'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}： {1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
			data_list = [subject, '疾病描述', '；'.join(list(set(desc))[:self.num_limit])]

		elif question_type == 'disease_complication':
			desc = [i['n.name'] for i in answers]
			# desc2 = [i['m.name'] for i in answers]
			subject = answers[0]['m.name']
			# desc = [i for i in desc1 + desc2 if i != subject]
			final_answer = '{0}的并发症包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
			data_list = [subject, '并发症', '；'.join(list(set(desc))[:self.num_limit])]

		elif question_type == 'disease_avoid_food':
			desc = [i['n.name'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}忌食的食物包括有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
			data_list = [subject, '忌食食物', '；'.join(list(set(desc))[:self.num_limit])]

		elif question_type == 'disease_good_food':
			do_desc = [i['n.name'] for i in answers if i['r.name'] == '宜吃']
			recommand_desc = [i['n.name'] for i in answers if i['r.name'] == '推荐食谱']
			subject = answers[0]['m.name']
			final_answer = '{0}宜食的食物包括有：{1}\n推荐食谱包括有：{2}'.format(subject, ';'.join(list(set(do_desc))[:self.num_limit]),
																 ';'.join(list(set(recommand_desc))[:self.num_limit]))
			data_list = [subject, '宜食食物', '；'.join(list(set(do_desc))[:self.num_limit])]

		elif question_type == 'food_avoid_disease':
			desc = [i['m.name'] for i in answers]
			subject = answers[0]['n.name']
			final_answer = '患有{0}的人最好不要吃{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)
			data_list = [subject, '不要吃的食物', '；'.join(list(set(desc))[:self.num_limit])]

		elif question_type == 'food_good_disease':
			desc = [i['m.name'] for i in answers]
			subject = answers[0]['n.name']
			final_answer = '患有{0}的人建议多试试{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)
			data_list = [subject, '建议吃的食物', '；'.join(list(set(desc))[:self.num_limit])]

		elif question_type == 'disease_drug':
			desc = [i['n.name'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}通常的使用的药品包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
			data_list = [subject, '使用药品', '；'.join(list(set(desc))[:self.num_limit])]

		elif question_type == 'drug_disease':
			desc = [i['m.name'] for i in answers]
			subject = answers[0]['n.name']
			final_answer = '{0}主治的疾病有{1},可以试试'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
			data_list = [subject, '治疗疾病', '；'.join(list(set(desc))[:self.num_limit])]

		elif question_type == 'disease_check':
			desc = [i['n.name'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}通常可以通过以下方式检查出来：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
			data_list = [subject, '检查项目', '；'.join(list(set(desc))[:self.num_limit])]

		elif question_type == 'check_disease':
			desc = [i['m.name'] for i in answers]
			subject = answers[0]['n.name']
			final_answer = '通常可以通过{0}检查出来的疾病有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
			data_list = [subject, '检查疾病', '；'.join(list(set(desc))[:self.num_limit])]

		elif question_type == 'disease_department':
			desc = [i['n.name'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}所属科室为： {1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
			data_list = [subject, '所属科室', '；'.join(list(set(desc))[:self.num_limit])]
		elif question_type == 'disease_treat_cost':
			desc = [i['m.treat_cost'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}的治疗费用相关信息：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
			data_list = [subject, '治疗费用', '；'.join(list(set(desc))[:self.num_limit])]
		elif question_type == 'disease_medical_insurance':
			desc = [i['m.medical_insurance'] for i in answers]
			subject = answers[0]['m.name']
			if '是' in desc:
				final_answer = '{0}是医保疾病'.format(subject)
				data_list = [subject, '属于', '医保']
			else:
				final_answer = '{0}不是医保疾病'.format(subject)
				data_list = [subject, '不属于', '医保']
		elif question_type == 'disease_transmission_way':
			desc = [i['m.transmission_way'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}的传播方式：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
			data_list = [subject, '传播方式', '；'.join(list(set(desc))[:self.num_limit])]

		elif question_type == 'disease_nursing_way':
			desc = [i['m.nursing'] for i in answers]
			subject = answers[0]['m.name']
			final_answer = '{0}的护理方法：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
			data_list = [subject, '护理方法', '；'.join(list(set(desc))[:self.num_limit])]

		res['final_answer'] = final_answer
		res['data_list'] = data_list
		return res
