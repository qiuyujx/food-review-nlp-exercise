import os
import click
from food_senti import train_model, make_prediction

# Constants
model_dir = '.\\model\\'

@click.command()
@click.option('--train', '-t', help='Train a model using a TSV (Tab Separated Values) file. \neg: "my_train.txt"')
@click.option('--model', '-m', default='default_model', help='The name of the model. **IMPORTANT: This will be output filename for training mode. \neg: "my_model"')
@click.option('--question', '-q', help='Enter any review text to be classified as positive or negative. If no model name (-m) is given, the "default_model" will be used. \neg: "Wow! Loved this place!"')
def main(train, model, question):
    if train:
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        train_model(train, model)
    elif question:
        make_prediction(question, model)
    else:
        print('\n\nInvalid options, please check help manual below:')
        click.echo(click.get_current_context().get_help())

if __name__ == '__main__':
    main()
