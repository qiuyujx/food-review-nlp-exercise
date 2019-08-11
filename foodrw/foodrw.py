'''foodrw.foodrw: main entry of the cli app'''

__version__ = '0.1.0'


import os
import click
from .foodrw_func import train_model, pred_text, pred_file

# Constants
model_dir = '.\\model\\'

# Helper functions
def validate_model(model):
    path_c = os.path.join(model_dir, model + '.classifier')
    path_w = os.path.join(model_dir, model + '.words')
    if os.path.exists(path_c) and os.path.exists(path_c):
        return True
    print('Error: Model "%s" is not found in ./model/ directory. Please train a model using "foodrw -t <training_file>" or use "foodrw -l" to view all the available models' % model)
    return False

@click.command()
@click.option('--train', '-t', help='Train a model using a TSV (Tab Separated Values) file. \neg: "my_train.txt"')
@click.option('--model', '-m', default='default_model', help='The name of the model. **IMPORTANT: This will be output filename for training mode. \neg: "my_model"')
@click.option('--question', '-q', help='Enter any review text to be classified as positive or negative. If no model name (-m) is given, the "default_model" will be used. \neg: "Wow! Loved this place!"')
@click.option('--srcfile', '-f', help='Classify multiple reivews in a text file. If "-m" is not specified, default model will be used. If "-d" is not specified, a default file name with suffix "_classified" will be generated. \neg: "my_test.txt"')
@click.option('--destfile', '-d', help='Destination file name when classifing multiple reviews in a text file. The format of this file will be TSV. \neg: "my_classified.txt"')
@click.option('--listmodel', '-l', is_flag=True, help='List all the available models.')
def main(train, model, question, srcfile, destfile, listmodel):
    print("\nWelcome! Food Review Sentiment Classifier %s." % __version__)
    if train:
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        train_model(train, model)
    
    elif question:
        if validate_model(model):
            pred_text(question, model)
    
    elif srcfile:
        if validate_model(model):
            if not destfile:
                f_comps = srcfile.split('.')
                destfile = f_comps[0] + '_classified.' + f_comps[1]
            pred_file(srcfile, model, destfile)
    
    elif listmodel:
        files = [f for f in os.listdir(model_dir) if os.path.isfile(os.path.join(model_dir, f))]
        f_classifiers = [f for f in files if f.endswith('.classifier')]
        print('\nCurrent available models: \n')
        if len(f_classifiers) == 0:
            print('There is no model available. Please run "foodrw -t <training_file>" to train a model')
        for f in f_classifiers:
            f_name = os.path.join(model_dir, f)
            model_name = os.path.splitext(f)[0]
            print(model_name)
            if not os.path.exists(os.path.join(model_dir, model_name + '.words')):
                print('*** Warning! The model "%s" lost its component which won\'t work properly' % model_name)
    
    else:
        print('\n\nInvalid options, please check help manual below:')
        click.echo(click.get_current_context().get_help())

if __name__ == '__main__':
    main()
