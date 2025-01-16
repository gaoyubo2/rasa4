from rasa.nlu.convert import convert_training_data
input_file = './data/rasa_dataset_training.json'
output_file = 'nlu_training.yml'
convert_training_data(data_file=input_file, out_file=output_file, output_format="md", language="zh")