#from base_imports import *
#from history_manager import HistoryManager
import uuid
from datetime import datetime
from gnowsys_ndf.ndf.gstudio_es.es import *
#from gnowsys_ndf.settings import GSTUDIO_ELASTIC_SEARCH,GSTUDIO_ELASTIC_SEARCH_IN_NODE_CLASS

connections.create_connection(hosts=['10.1.0.219:9200'])

class Node(DocType):
	type= Text()
	name = Text()
	altnames = Text()
	plural = Text()
	prior_node = Text()
	post_node = Text()
	language = Text()
	type_of = Text()
	member_of = Text()
	access_policy = Text()
	created_at = Date()
	created_by = Long()
	last_update = Date()
	modified_by = Long()
	contributors = Text()
	location = Text()
	content = Text()
	content_org = Text()
	group_set = Text()
	collection_set = Text()
	property_order = Text()
	start_publication = Date()
	tags = Text()
	featured = Text()
	url = Text()
	comment_enabled = Text()
	login_required = Text()
	status = Text()
	rating = Text()
	snapshot = Text()

	class Meta:
	    index = 'nodes'
	    doc_type = 'gsystem'

	def validation(self):
		if self.id in [None,'']:
			raise ValueError("UUID should not be empty")
		elif self.meta.id in [None,'']:
			raise ValueError("ES ID(META ID) should not be empty")
		elif self.access_policy not in ['PUBLIC','PRIVATE']:
			raise ValueError("access_policy should be PUBLIC OR PRIVATE")
		elif self.name in [None, '']:
			raise ValueError("name should not be empty")
		elif self.type in [None,'']:
			raise ValueError("type should not be empty")
		elif self.type not in ['Filehive','GAttribute', 'GRelation', 'Buddy', 'Benchmark', 'MetaType', 'GSystemType', 'RelationType', 'AttributeType', 'GSystem', 'Group', 'ToReduceDocs', 'Author','Counter']:
			raise ValueError("Not a valid type")

	def save(self, **kwargs):
		self.id = uuid.uuid4()
		self.meta.id=self.id
		print self.id
		print self.meta.id
		self.access_policy = "PUBLIC"
		self.type = "GSystem"
		self.created_at = datetime.datetime.now()
		self.language = ["en","English" ]
		self.validation()
		return super(Node,self).save(**kwargs)

	def add_in_group_set(self, group_id):
		if group_id not in self.group_set:
		    self.group_set.append(group_id)
		return self

