import numpy as np
#################################
#	CNN layer
#################################
class conv(object):

	def __init__(self,input_size=-1,output_size=None,kernel_size=None,post=None):

		self.__name__ = 'conv'
		self.input_size = input_size
		self.output_size =  output_size
		self.kernel_size = kernel_size
		self.post = post
		

	def __def_str__(self,ilayer):
		if ilayer == 0:
			return 'self.convlayer_%03d = nn.Conv3d(input_shape[0],%d,kernel_size=%d)' %(ilayer,self.output_size,self.kernel_size)
		else:
			return 'self.convlayer_%03d = nn.Conv3d(%d,%d,kernel_size=%d)' %(ilayer,self.input_size,self.output_size,self.kernel_size)

	def __use_str__(self,ilayer):
		if self.post is None:
			return 'x = self.convlayer_%03d(x)' %ilayer
		elif isinstance(self.post,str):
			return 'x = F.%s(self.convlayer_%03d(x))' %(self.post,ilayer)
		else:
			print('Error with post processing of conv layer %d' %ilayer)
			return 'x = self.convlayer_%03d(x)' %ilayer

	def __get_params__(self):
		params = {}
		params['name'] = self.__name__
		params['input_size'] = self.input_size
		params['output_size'] = self.output_size
		params['kernel_size'] = self.kernel_size
		params['post'] = self.post
		return params

	def __init_from_dict__(self,params):
		self.input_size = params['input_size']
		self.output_size =  params['output_size']
		self.kernel_size = params['kernel_size']
		self.post = params['post']

	def __human_readable_str__(self,ilayer):
		return '#conv layer % 3d: conv | input % 2d  output % 2d  kernel % 2d  post %s' %(ilayer,self.input_size,self.output_size,self.kernel_size,self.post)

#################################
#	POOL layer
#################################
class pool(object):

	def __init__(self,kernel_size=None,post=None):
		self.__name__ = 'pool'
		self.kernel_size = kernel_size
		self.post = post

	def __def_str__(self,ilayer):
		return 'self.convlayer_%03d = nn.MaxPool3d((%d,%d,%d))' %(ilayer,self.kernel_size,self.kernel_size,self.kernel_size)

	def __use_str__(self,ilayer):
		if self.post is None:
			return 'x = self.convlayer_%03d(x)' %ilayer
		elif isinstance(self.post,str):
			return 'x = F.%s(self.convlayer_%03d(x))' %(self.post,ilayer)
		else:
			print('Error with post processing of conv layer %d' %ilayer)
			return 'x = self.convlayer_%03d(x)' %ilayer

	def __get_params__(self):
		params = {}
		params['name'] = self.__name__
		params['kernel_size'] = self.kernel_size
		params['post'] = self.post
		return params

	def __init_from_dict__(self,params):
		self.kernel_size = params['kernel_size']
		self.post = params['post']

	def __human_readable_str__(self,ilayer):
		return '#conv layer % 3d: pool | kernel % 2d  post %s' %(ilayer,self.kernel_size,self.post)

#################################
#	dropout layer
#################################
class dropout(object):

	def __init__(self,percent=0.5):
		self.__name__ = 'dropout'
		self.percent=percent

	def __def_str__(self,ilayer):
		return 'self.convlayer_%03d = nn.Dropout3d(%0.1f)' %(ilayer,self.percent)

	@staticmethod
	def __use_str__(ilayer):
		return 'x = self.convlayer_%03d(x)' %ilayer

	def __get_params__(self):
		params = {}
		params['name'] = self.__name__
		params['percent'] = self.percent
		return params

	def __init_from_dict__(self,params):
		self.percent = params['percent']

	def __human_readable_str__(self,ilayer):
		return '#conv layer % 3d: drop | percent %0.1f' %(ilayer,self.percent)

#################################
#	fully connected layer
#################################
class fc(object):

	def __init__(self,input_size=-1,output_size=None,post=None):

		self.__name__ = 'fc'
		self.input_size = input_size
		self.output_size = output_size
		self.post = post

	def __def_str__(self,ilayer):
		if ilayer == 0:
			return 'self.fclayer_%03d = nn.Linear(size,%d)' %(ilayer,self.output_size)
		else:
			return 'self.fclayer_%03d = nn.Linear(%d,%d)' %(ilayer,self.input_size,self.output_size)

	def __use_str__(self,ilayer):
		if self.post is None:
			return 'x = self.fclayer_%03d(x)' %ilayer
		elif isinstance(self.post,str):
			return 'x = F.%s(self.fclayer_%03d(x))' %(self.post,ilayer)
		else:
			print('Error with post processing of conv layer %d' %ilayer)
			return 'x = self.fclayer_%03d(x)' %ilayer

	def __get_params__(self):
		params = {}
		params['name'] = self.__name__
		params['input_size'] = self.input_size
		params['output_size'] = self.output_size
		params['post'] = self.post
		return params

	def __init_from_dict__(self,params):
		self.input_size = params['input_size']
		self.output_size =  params['output_size']
		self.post = params['post']

	def __human_readable_str__(self,ilayer):
		return '#fc   layer % 3d: fc   | input % 2d  output % 2d  post %s' %(ilayer,self.input_size,self.output_size,self.post)

#################################
#
#	MODEL GENERATOR
#
#################################
class NetworkGenerator(object):

	def __init__(self,name='_tmp_model_',fname='_tmp_model_.py',conv_layers=None,fc_layers=None):

		# name of the model
		self.name = name

		# filename
		self.fname = fname

		# structure of the convolutional/fc layers
		self.conv_layers = conv_layers or []
		self.fc_layers = fc_layers or []

		# dimension of the final fc layer
		self.final_dim = 1

		# possible number of randomly generated conv/fc layers
		self.num_conv_layers = range(1,11)
		self.num_fc_layers = range(1,5)

		# possible types of conv layers
		self.conv_types = ['conv','dropout','pool']

		# conv parameters
		self.conv_params = {}
		self.conv_params['output_size'] = range(1,10)
		self.conv_params['kernel_size'] = range(2,5)

		# pool parameters
		self.pool_params = {}
		self.pool_params['kernel_size'] = range(2,5)

		# params of the dropout layers
		self.dropout_params = {}
		self.dropout_params['percent'] = np.linspace(0.1,0.9,9)

		# params for the automatic generation of fc layers
		self.fc_params = {}
		self.fc_params['output_size'] = [2**i for i in range(4,11)]	

		# types of post processing
		# must be in torch.nn.functional
		self.post_types = [None,'relu']

	#######################################
	#
	# Routines used to write dow the 
	# file containing the model
	#
	#######################################

	def write(self):

		f = open(self.fname,'w')
		self._write_import(f)
		self._write_definition(f)
		self._write_init(f)
		self._write_conv_output(f)
		self._write_forward_feature(f)
		self._write_forward(f)
		f.close()

	@staticmethod
	# import statement
	def _write_import(fhandle):

		modules = '''import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data as data_utils

'''

		fhandle.write(modules)

	# comment and such
	def _write_definition(self,fhandle):
		ndash = 70
		fhandle.write('#'*ndash+'\n#\n')
		fhandle.write('# Model automatically generated by modelGenerator\n')
		fhandle.write('#\n'+'#'*ndash+'\n\n')

		fhandle.write('#'+'-'*ndash+'\n')
		fhandle.write('# Network Structure\n')
		fhandle.write('#'+'-'*ndash+'\n')
		for ilayer,layer in enumerate(self.conv_layers):
			fhandle.write('%s\n' %layer.__human_readable_str__(ilayer))
		for ilayer,layer in enumerate(self.fc_layers):
			fhandle.write('%s\n' %layer.__human_readable_str__(ilayer))
		fhandle.write('#'+'-'*ndash+'\n\n')

	# initialization of the  model
	# here all the layers are defined
	def _write_init(self,fhandle):
		fhandle.write('class ' + self.name + '(nn.Module):\n')
		fhandle.write('\n')
		fhandle.write('\tdef __init__(self,input_shape):\n')
		fhandle.write('\t\tsuper(%s,self).__init__()\n' %(self.name))
		fhandle.write('\n')

		# write the conv layer
		for ilayer,layer in enumerate(self.conv_layers):
			fhandle.write('\t\t%s\n' %layer.__def_str__(ilayer))

		# the size determination between the conv and fc blocks
		fhandle.write('\n')
		fhandle.write('\t\tsize = self._get_conv_output(input_shape)\n')
		fhandle.write('\n')

		# write the fc layers
		for ilayer,layer in enumerate(self.fc_layers):
			fhandle.write('\t\t%s\n' %layer.__def_str__(ilayer))
		fhandle.write('\n')

	@staticmethod
	# get the size of the output at the end of the conv block
	def _write_conv_output(fhandle):
		func = '''
\tdef _get_conv_output(self,shape):
\t\tinp = Variable(torch.rand(1,*shape))
\t\tout = self._forward_features(inp)
\t\treturn out.data.view(1,-1).size(1)

'''
		fhandle.write(func)

	# forward feature conatining all the conv layers
	# here all the conv layers are defined
	def _write_forward_feature(self,fhandle):
		fhandle.write('\tdef _forward_features(self,x):\n')
		for ilayer,layer in enumerate(self.conv_layers):
			fhandle.write('\t\t%s\n' %layer.__use_str__(ilayer))
		fhandle.write('\t\treturn x\n')
		fhandle.write('\n')

	# total forward pass
	# here _forward_features is used
	# and all the fc layers are used
	def _write_forward(self,fhandle):
		fhandle.write('\tdef forward(self,x):\n')
		fhandle.write('\t\tx = self._forward_features(x)\n')
		fhandle.write('\t\tx = x.view(x.size(0),-1)\n')
		for ilayer,layer in enumerate(self.fc_layers):
			fhandle.write('\t\t%s\n' %layer.__use_str__(ilayer))
		fhandle.write('\t\treturn x\n')
		fhandle.write('\n')

	# print the definition of the network to screen
	def print(self):
		ndash = 70

		print('#'+'-'*ndash)
		print('# Network Structure')
		print('#'+'-'*ndash)
		for ilayer,layer in enumerate(self.conv_layers):
			print('%s' %layer.__human_readable_str__(ilayer))
		for ilayer,layer in enumerate(self.fc_layers):
			print('%s' %layer.__human_readable_str__(ilayer))
		print('#'+'-'*ndash+'\n')

	#########################################
	#
	# get a new random model
	#
	#########################################
	def get_new_random_model(self):

		# number of conv/fc layers
		nconv = np.random.choice(self.num_conv_layers)	
		nfc   = np.random.choice(self.num_fc_layers)	

		# generate the conv layers
		self.conv_layers = []
		for ilayer in range(nconv):
			self._init_conv_layer_random(ilayer)

		# generate the fc layers
		self.fc_layers = []
		for ilayer in range(nfc):
			self._init_fc_layer_random(ilayer)

		# fix the final dimension
		self.fc_layers[-1].output_size = self.final_dim


	# pick a layer type
	def _init_conv_layer_random(self,ilayer):

		# determine wih type of layer we want
		# first layer is a conv
		# we can't have 2 pool in a row
		if ilayer == 0:
			name = self.conv_types[0]

		# if rpevious layer is pool, next can't be pool
		elif self.conv_layers[ilayer-1].__name__ == 'pool':
			name = np.random.choice(self.conv_types[:-1])

		# else it can be anything
		else: 
			name = np.random.choice(self.conv_types)

		# init the parms of the layer
		# each layer type has its own params
		# the output/input size matching is done automatically
		if name == 'conv':
			params = {}
			params['name'] = name

			if ilayer == 0:
				params['input_size'] = -1 #fixed by input shape
			else:
				for isearch in range(ilayer-1,-1,-1):
					if self.conv_layers[isearch].__name__ == 'conv':
						params['input_size'] = self.conv_layers[isearch].output_size
						break

			params['output_size'] = np.random.choice(self.conv_params['output_size'])
			params['kernel_size'] = np.random.choice(self.conv_params['kernel_size'])
			params['post'] = np.random.choice(self.post_types)
			
		if name == 'pool':
			params = {}
			params['name'] = name
			params['kernel_size'] = np.random.choice(self.pool_params['kernel_size'])
			params['post'] = np.random.choice(self.post_types)


		if name == 'dropout':
			params = {}
			params['name'] = name
			params['percent'] = np.random.choice(self.dropout_params['percent'])

		# create the current layer class instance
		# and initialize if with the __init_from_dict__() method
		current_layer = eval(params['name'])()
		current_layer.__init_from_dict__(params)
		self.conv_layers.append(current_layer)

	def _init_fc_layer_random(self,ilayer):

		# init the parms of the layer
		# each layer type has its own params
		# the output/input size matching is done automatically
		name = 'fc' # so far only fc layer here
		params = {}
		params['name'] = name
		if ilayer == 0:
			params['input_size'] = -1 # fixed by the conv layers
		else:
			params['input_size'] = self.fc_layers[ilayer-1].output_size

		params['output_size'] = np.random.choice(self.fc_params['output_size'])
		params['post'] = np.random.choice(self.post_types)


		current_layer = eval(params['name'])()
		current_layer.__init_from_dict__(params)
		self.fc_layers.append(current_layer)




if __name__== '__main__':


	conv_layers = []
	conv_layers.append(conv(output_size=4,kernel_size=2,post='relu'))
	conv_layers.append(pool(kernel_size=2))
	conv_layers.append(conv(input_size=4,output_size=5,kernel_size=2,post='relu'))
	conv_layers.append(pool(kernel_size=2))

	fc_layers = []
	fc_layers.append(fc(output_size=84,post='relu'))
	fc_layers.append(fc(input_size=84,output_size=1))

	MG = NetworkGenerator(name='cnntest',fname='model.py',conv_layers=conv_layers,fc_layers=fc_layers)
	MG.print()
	MG.write()

	# MGR = NetworkGenerator(name='cnnrand',fname='modelrandom.py')
	# MGR.get_new_random_model()
	# MGR.print()
	# MGR.write()