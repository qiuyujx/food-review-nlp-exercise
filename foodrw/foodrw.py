'''foodrw.foodrw: main entry of the cli app'''

__version__ = '0.1.0'


import os
import click
from .foodrw_func import train_model, pred_text, pred_file

# Constants
model_dir = '.\\model\\'

@click.command()
@click.option('--train', '-t', help='Train a model using a TSV (Tab Separated Values) file. \neg: "my_train.txt"')
@click.option('--model', '-m', default='default_model', help='The name of the model. **IMPORTANT: This will be output filename for training mode. \neg: "my_model"')
@click.option('--question', '-q', help='Enter any review text to be classified as positive or negative. If no model name (-m) is given, the "default_model" will be used. \neg: "Wow! Loved this place!"')
@click.option('--srcfile', '-f', help='Classify multiple reivews in a text file. If "-m" is not specified, default model will be used. If "-d" is not specified, a default file name with suffix "_classified" will be generated. \neg: "my_test.txt"')
@click.option('--destfile', '-d', help='Destination file name when classifing multiple reviews in a text file. The format of this file will be TSV. \neg: "my_classified.txt"')
def main(train, model, question, srcfile, destfile):
    print("Welcome! Food Review Sentiment Classifier %s." % __version__)
    if train:
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        train_model(train, model)
    elif question:
        pred_text(question, model)
    elif srcfile:
        if not destfile:
            f_comps = srcfile.split('.')
            destfile = f_comps[0] + '_classified.' + f_comps[1]
        pred_file(srcfile, model, destfile)
    else:
        print('\n\nInvalid options, please check help manual below:')
        click.echo(click.get_current_context().get_help())

if __name__ == '__main__':
    main()
