from gnowsys_ndf.ndf.gstudio_es.es import *

connections.create_connection(hosts=['10.1.0.219:9200'])

class Benchmark(DocType):

  type=Text(fielddata=True)
  name= Text(fielddata=True)
  time_taken = Text(fielddata=True)
  parameters = Text(fielddata=True)
  size_of_parameters = Text(fielddata=True)
  function_output_length = Text(fielddata=True)
  last_update = Text(fielddata=True)
  action = Text(fielddata=True)
  user = Text(fielddata=True)
  session_key = Text()
  group =Text(fielddata=True)
  has_data = Text()

  class Meta:
    index = 'benchmarks'
    doc_type = 'benchmark'

  def validation(self):
    if self.id in [None,'']:
      raise ValueError("UUID should not be empty")
    elif self.meta.id in [None,'']:
      raise ValueError("ES ID(META ID) should not be empty")
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
    return super(Benchmark,self).save(**kwargs)


  def __unicode__(self):
    return self.id

  def identity(self):
    return self.__unicode__()
