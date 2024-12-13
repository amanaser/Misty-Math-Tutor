import os,sys
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
os.environ['IRASA'] = '/home/slimuser/Desktop/HRI/misty project/incremental_rasa_nlu'
sys.path.append(os.environ['IRASA'])

from rasa.model_training import train

train(
        domain='domain_colors.yml',
        config='config.yml',
        training_files='data_colors/',
        output='models_colors/'
)