from gnowsys_ndf.ndf.models import *
from gnowsys_ndf.settings import *
from gnowsys_ndf.ndf.gstudio_es.es import *
import json



class Mapper(Object):

	global must_list
	global should_list
	global temp_string
	must_list = ""
	should_list =""
	temp_string = ""

	def is_empty(self,any_structure):
		if any_structure:
			if isinstance(any_structure,list):
				if len(any_structure) == 0:
					return True
				else:
				 	return False
				return False
		else:
			return True

	def is_list1(self,key,value,get_should_or_must_list):
		# print must_list
		# print ""
		global must_list
		global should_list
		global temp_string
		import ast
		print "call is_list"
		for t_list in value:
			print "~~~~~~~~~~~~~~~~~~~"
			print t_list
			print "~~~~~~~~~~~~~~~~~~~"
			for k,v in t_list.iteritems():
				if k == "$and" or k == "$or":
					print "if condtion"
					print value
					value.sort()
					print value
					print "======================================="
				break
			break

		print value
		print "``````````````````````````````````````````````"
		temp1 =""
		temp2=""
		if isinstance(value,dict):
			value = json.loads(value)
		for t_list in value:
			print "88888888888888888888888888888888888888888888888888888888888888888888888888888"
			print value
			t_list= str(t_list)
			print t_list
			if not isinstance(t_list,dict) and t_list.startswith("{"):
				print t_list
				# t_list = json.dumps(t_list)
				# eval(t_list)
				# dict(t_list)
			 	t_list = ast.literal_eval(t_list)
			 	print t_list
			 	print "literal_eval executed"
			# elif isinstance(t_list,str) and not t_list.startswith("{"):
			#   	pass
			for k,v in t_list.iteritems():
				print "111111111111111111111111111111111"
				print k
				print "111111111111111111111111111111111"
				print v
				if "." in k:
					k = k.replace(".","__")
				if isinstance(v,dict) and "$regex" in str(v):
					v = v["$regex"]
				# if isinstance(v,list):
				# 	v.sort()
				if isinstance(v,dict) and "$all" in str(v):
					print "$$$$$$$$$$$$$AAAAAAAAAAAAAAAAAAAAALLLLLLLLLLLLLLLLLLL"
					t = ','.join("'"+str(v)+"'" for v in v["$all"])
					print t
					temp2+="Q('terms',"+k+"=["+str(t)+"]),"
				if "$and" in k:
					return temp1+"Q('bool',must=["+self.is_list1(k,v,get_should_or_must_list=value)+"])"
				elif "$or" in k:
					return temp1+"Q('bool',should=["+self.is_list1(k,v,get_should_or_must_list=value)+"])"
				elif k != "$or" and k != "$and":
					print "lsat block executed"
					temp1 +="Q('match',"+str(k)+"='"+str(v)+"'),"
					print temp1
		return temp2 + temp1
		#return get_should_or_must_list
		

	


	def ESQuery(self,*args,**kwargs):
		global must_list
		global should_list
		global temp_string

		
		collection = ""
		if kwargs.get('node', None):
			node = kwargs.get('node', None)
			collection = "node"
		elif kwargs.get('triple', None):
			collection = "triple"
		elif kwargs.get('benchmark', None):
			node = kwargs.get('benchmark', None)
			collection = "benchmark"
		print node
		minimum_should_match = kwargs.get('minimum_should_match', None)
		self.node = node
		self.minimum_should_match = minimum_should_match
		mongo_dict = {}
		if kwargs.get('findone', None):
			dict_values = node
			mongo_dict.update(node)
		else:
			dict_values =  self.node.__dict__
			for k,v in dict(dict_values).items():
				if "_Cursor__spec" in k:
					mongo_dict.update(v)

		converted_es_query = ""
		print dict_values


		#print mongo_dict

		bool_str = "Q('bool',"
		if minimum_should_match:
			bool_end_str = ",minimum_should_match="+str(minimum_should_match)+")"
		else:
			bool_end_str = ",minimum_should_match=1)"
		for key,value in mongo_dict.iteritems():
			print "mainnnnnnnnnnnnnnnnnnnnnnnnnnn forrrrrrrrrrrrrrrrrrr loopppppppppppppppppp"
			print key
			if key and value:
				if "." in key:
					key = key.replace(".","__")
				if key == "$and" and not self.is_empty(value):
					print "$and-------------------------"
					if isinstance(value,list):
						print "$and--------------------------------------"
						print value
						must_list = self.is_list1(key,value,must_list)

				elif key == "$or" and not self.is_empty(value):
					print "$or-------------------------"
					if isinstance(value,list):
						print "list--------------------------------------"
						print value
						should_list = self.is_list1(key,value,should_list)

				elif key != "$or" and key != "$and":
					if "$in" in value:
						t = ','.join("'"+str(v)+"'" for v in value["$in"])
						must_list+="Q('terms',"+key+"=["+str(t)+"]),"
					elif "$all" in value:
						t = ','.join("'"+str(v)+"'" for v in value["$all"])
						must_list+="Q('terms',"+key+"=["+str(t)+"]),"
					else:
						if "$exists" in value:
							must_list+="Q('exists',field='"+key+"'),"
						else:
							if must_list and not kwargs.get('findone', None):
								must_list+=",Q('match',"+str(key)+"='"+str(value)+"'),"
							else:
								must_list+="Q('match',"+str(key)+"='"+str(value)+"'),"

			#temp_list.append("Q('match',"+key+"='"+value+"')")

		print must_list
		print "must above"
		print should_list
		print "should"

		if should_list:
			q = bool_str + "must=[" +must_list +"],should=[" +  should_list + "]"+bool_end_str
			print q
		else:
			q = bool_str + "must=[" +must_list +"])"
			print q
		if collection == "node":
			es_result = Search(using=es, index="nodes",doc_type="gsystemtype,gsystem,metatype,relationtype,attribute_type,group,author").query(eval(q))
		elif collection == "benchmark":
			es_result = Search(using=es, index="benchmarks",doc_type="benchmark").query(eval(q))

		must_list = ""
		should_list =""
		temp_string = ""
		return es_result