# Initial goal of the project

This project was initiated by my Le Wagon classmate, Tristan Lanson
(`github.com/lansoni`). The goal was to generate 'Bach-like' music using a set of
MIDI files of his *"Well-tempered clavier"* corpus to train a neural network. My
partners on the project focused on training a 'classical' LSTM model, while I
set on modelling a transformer model using tensorflow (and Keras) based on the original
paper 'Attention is all you need'

# Implementation

We use (for the most part) custom classes and function as well as the Keras layer
API whenever possible.

Contrary to most AI music generation, our prediction space
contains the **whole 'space' of the piano keys**: at each time step, any keys can be pressed,
(`2**64` possibilities) not just those forming a 'chord'. This is to accomodate
Bach's work specificities, based on **pich variations rather than chord progression**,
so we wanted to let the model 'choose' freely amongst all possibilities.

This calls for a sigmoid ouput for all features, rather than a softmax applied on
the classes space.

## Loss and model evaluation

To evaluate the model, we have to account for the 'musicality' of the result. We
decided to go for a comparison of a **gaussian blurred** version of the predicted ouput vs.
an also blurred version of the true output, which should account for a good rating of
the general movement of the piece.

The loss function evalutes probabilities, so this calls for an averaged **binary crossentropy**
for each piano key and each time step. We don't blur in this case as this would
only result in leading the model to predict multiple adjacent notes played together,
which is very dissonant to human ears.

# Training and results

Training was made locally using my GTX1060 and nVidia CUDA capabilities, in about
8 hours. We obtained a **>90% accuracy score**, compared to 55% on our base LSTM model.
More importantly, the results were subjectively very satisfying, with reproduction of
patterns typical of Bach's work.
