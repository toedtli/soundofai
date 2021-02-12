# -*- coding: utf-8 -*-
"""text_embedders_benchmark_preview.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/toedtli/soundofai/blob/toedtli_mytestbranch/text_embedders_benchmark_preview.ipynb
"""

#!pip install tensorflow_text

#!nvidia-smi

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text  # Registers the ops.

from abc import ABC, abstractmethod

import time
import multiprocessing
from tqdm.notebook import tqdm

import json
import pandas as pd

class PredictionModel(ABC):
  @abstractmethod
  def build(self):
    """ 
      This method builds a pre-trained model
    """
    pass

  @abstractmethod
  def predict(self, sentences):
    """
      Applies the built model to the given input sentences

      :param: sentences: an iterable of N strings

      :returns: an NxK numpy matrix where K is the embedding size
    """
    pass

  
  def additional_infos(self):
    """
      Provides additional informations that may be useful to track
      :returns: dictionary str->[str|number]
                example: {"family":"BERT","word_level_output_available":True}
    """
    return {}

# Peculiar models that need more time to code:
# https://tfhub.dev/google/LaBSE/1

# Other models that do not fit our needs
# question-answer models
#   https://tfhub.dev/google/universal-sentence-encoder-multilingual-qa/3
#   https://tfhub.dev/google/universal-sentence-encoder-qa/3
# Specific for medical field
#   https://tfhub.dev/google/experts/bert/pubmed/2
#   https://tfhub.dev/google/experts/bert/pubmed/squad2/2


class HubPredictionModelWithPreprocessor(PredictionModel):
  preprocessor_url=""
  tf_hub_url=""
  family=""

  def build(self):
    text_input = tf.keras.layers.Input(shape=(), dtype=tf.string)
    preprocessor = hub.KerasLayer(self.preprocessor_url)
    encoder_inputs = preprocessor(text_input)
    encoder = hub.KerasLayer(self.tf_hub_url, trainable=False)
    outputs = encoder(encoder_inputs)
    pooled_output = outputs["pooled_output"]      # [batch_size, 1024].
    sequence_output = outputs["sequence_output"]  # [batch_size, seq_length, 1024].

    self.model = tf.keras.Model(text_input, pooled_output)
  
  def predict(self, sentences):
    sentences_tensor = tf.constant(sentences)
    output_tensor = self.model(sentences_tensor)
    return output_tensor.numpy()

  def additional_infos(self):
    return {
        "preprocessor_url":self.preprocessor_url,
        "tf_hub_url":self.tf_hub_url,
        "family":self.family,
        "word_level_output_available":True
    }
  

class talkheads_ggelu_bert_en_large(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/talkheads_ggelu_bert_en_large/1"


class bert_en_uncased_L12_H768_A12(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/3"


class small_bert_en_uncased_L4_H512_A8(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-512_A-8/1"


class bert_en_uncased_L2_H128_A2(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-128_A-2/1"


class bert_en_uncased_L24_H1024_A16(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/bert_en_uncased_L-24_H-1024_A-16/3"


class bert_en_cased_L12_H768_A12(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/bert_en_cased_L-12_H-768_A-12/3"


class bert_en_uncased_L2_H512_A8(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-512_A-8/1"


class bert_en_uncased_L4_H128_A2(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-128_A-2/1"


class bert_en_uncased_L2_H768_A12(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-768_A-12/1"


class bert_en_uncased_L2_H256_A4(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-256_A-4/1"


class lambert_en_uncased_L24_H1024_A16(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/lambert_en_uncased_L-24_H-1024_A-16/1"


class small_bert_en_uncased_L12_H768_A12(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-12_H-768_A-12/1"


class bert_en_uncased_L4_H256_A4(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-256_A-4/1"


class bert_en_uncased_L4_H768_A12(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-768_A-12/1"


class bert_en_uncased_L8_H512_A8(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-8_H-512_A-8/1"


class bert_en_cased_L24_H1024_A16(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_cased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/bert_en_cased_L-24_H-1024_A-16/3"


class bert_en_wwm_cased_L24_H1024_A16(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_cased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/bert_en_wwm_cased_L-24_H-1024_A-16/3"


class bert_en_uncased_L8_H256_A4(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-8_H-256_A-4/1"


class bert_en_uncased_L6_H256_A4(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-256_A-4/1"


class bert_en_uncased_L12_H512_A8(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-12_H-512_A-8/1"


class bert_en_uncased_L8_H128_A2(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-8_H-128_A-2/1"


class bert_en_wwm_uncased_L24_H1024_A16(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/bert_en_wwm_uncased_L-24_H-1024_A-16/3"


class bert_en_uncased_L12_H256_A4(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-12_H-256_A-4/1"


class talkheads_ggelu_bert_en_base(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/talkheads_ggelu_bert_en_base/1"


class bert_en_uncased_L8_H768_A12(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-8_H-768_A-12/1"


class bert_en_uncased_L6_H768_A12(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-768_A-12/1"


class bert_en_uncased_L6_H512_A8(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-512_A-8/1"


class bert_en_uncased_L6_H128_A2(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-128_A-2/1"


class bert_en_uncased_L12_H128_A2(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-12_H-128_A-2/1"


class bert_en_uncased_L10_H768_A12(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-10_H-768_A-12/1"


class bert_en_uncased_L10_H512_A8(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-10_H-512_A-8/1"


class bert_en_uncased_L10_H256_A4(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-10_H-256_A-4/1"


class bert_en_uncased_L10_H128_A2(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-10_H-128_A-2/1"


class bert_wiki_books(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url='https://tfhub.dev/google/experts/bert/wiki_books/2'


class bert_wiki_books_stt2(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/google/experts/bert/wiki_books/sst2/2"


class bert_wiki_books_squad2(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/google/experts/bert/wiki_books/squad2/2"


class bert_wiki_books_qqp(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/google/experts/bert/wiki_books/qqp/2"


class bert_wiki_books_qnli(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/google/experts/bert/wiki_books/qnli/2"


class bert_wiki_books_mnli(HubPredictionModelWithPreprocessor):
  family="BERT"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/google/experts/bert/wiki_books/mnli/2"




class HubPredictionModelWithPreprocessorAndDefaultSignature(PredictionModel):
  preprocessor_url=""
  tf_hub_url=""
  family=""

  def build(self):
    text_input = tf.keras.layers.Input(shape=(), dtype=tf.string)
    preprocessor = hub.KerasLayer(self.preprocessor_url)
    encoder_inputs = preprocessor(text_input)
    encoder = hub.KerasLayer(self.tf_hub_url, trainable=False)
    outputs = encoder(encoder_inputs)
    pooled_output = outputs["default"]      # [batch_size, emb_size].

    self.model = tf.keras.Model(text_input, pooled_output)
  
  def predict(self, sentences):
    sentences_tensor = tf.constant(sentences)
    output_tensor = self.model(sentences_tensor)
    return output_tensor.numpy()

  def additional_infos(self):
    return {
        "preprocessor_url":self.preprocessor_url,
        "tf_hub_url":self.tf_hub_url,
        "family": self.family,
        "word_level_output_available":False
    }


class UniversalSentenceEncoderCmlmEnBase(HubPredictionModelWithPreprocessorAndDefaultSignature):
  family="universal sentence encoder"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/google/universal-sentence-encoder-cmlm/en-base/1"


class UniversalSentenceEncoderCmlmMultilingualBaseBr(HubPredictionModelWithPreprocessorAndDefaultSignature):
  family="universal sentence encoder"
  preprocessor_url="https://tfhub.dev/google/universal-sentence-encoder-cmlm/multilingual-preprocess/2"
  tf_hub_url="https://tfhub.dev/google/universal-sentence-encoder-cmlm/multilingual-base-br/1"


class UniversalSentenceEncoderCmlmMultilingualBase(HubPredictionModelWithPreprocessorAndDefaultSignature):
  family="universal sentence encoder"
  preprocessor_url="https://tfhub.dev/google/universal-sentence-encoder-cmlm/multilingual-preprocess/2"
  tf_hub_url="https://tfhub.dev/google/universal-sentence-encoder-cmlm/multilingual-base/1"


class UniversalSentenceEncoderCmlm(HubPredictionModelWithPreprocessorAndDefaultSignature):
  family="universal sentence encoder"
  preprocessor_url="https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
  tf_hub_url="https://tfhub.dev/google/universal-sentence-encoder-cmlm/en-large/1"



class SimpleHubPredctionModel(PredictionModel):
  tf_hub_url=""
  family=""

  def build(self):
    self.model = hub.load(self.tf_hub_url)

  def predict(self, sentences):
    output_tensor = self.model(sentences)
    return output_tensor.numpy()

  def additional_infos(self):
    return {
        "tf_hub_url":self.tf_hub_url,
        "family": self.family,
        "word_level_output_available":False
    }


class UniversalSentenceEncoder(SimpleHubPredctionModel):
  family="universal sentence encoder"
  tf_hub_url="https://tfhub.dev/google/universal-sentence-encoder/4"


class UniversalSentenceEncoderMultilingual(SimpleHubPredctionModel):
  family="universal sentence encoder"
  tf_hub_url="https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"


class UniversalSentenceEncoderLarge(SimpleHubPredctionModel):
  family="universal sentence encoder"
  tf_hub_url="https://tfhub.dev/google/universal-sentence-encoder-large/5"


class UniversalSentenceEncoderMultilingualLarge(SimpleHubPredctionModel):
  family="universal sentence encoder"
  tf_hub_url="https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3"


class NnlmEnDim128(SimpleHubPredctionModel):
  family="NNLM"
  tf_hub_url="https://tfhub.dev/google/nnlm-en-dim128/2"


class NnlmEnDim128WithNormalization(SimpleHubPredctionModel):
  family="NNLM"
  tf_hub_url="https://tfhub.dev/google/nnlm-en-dim128-with-normalization/2"


class NnlmEnDim50(SimpleHubPredctionModel):
  family="NNLM"
  tf_hub_url="https://tfhub.dev/google/nnlm-en-dim50/2"


class NnlmEnDim50WithNormalization(SimpleHubPredctionModel):
  family="NNLM"
  tf_hub_url="https://tfhub.dev/google/nnlm-en-dim50-with-normalization/2"


class GnewsSwivel20dim(SimpleHubPredctionModel):
  family="Swivel matrix factorization"
  tf_hub_url="https://tfhub.dev/google/tf2-preview/gnews-swivel-20dim/1"


class WikiWords250(SimpleHubPredctionModel):
  family="Skipgram model"
  tf_hub_url="https://tfhub.dev/google/Wiki-words-250/2"


class WikiWords250WithNormalization(SimpleHubPredctionModel):
  family="Skipgram model"
  tf_hub_url="https://tfhub.dev/google/Wiki-words-250-with-normalization/2"


class WikiWords500(SimpleHubPredctionModel):
  family="Skipgram model"
  tf_hub_url="https://tfhub.dev/google/Wiki-words-500/2"


class WikiWords500WithNormalization(SimpleHubPredctionModel):
  family="Skipgram model"
  tf_hub_url="https://tfhub.dev/google/Wiki-words-500-with-normalization/2"

def benchmark_prediction_model(model_name, sentences, results=None):
  model=eval(f"{model_name}()")

  if results is None:
    results={}
  
  results["model_name"]=model_name
  
  print(f"{model_name} - building...")
  now=time.time()
  model.build()
  results["build_seconds"]=time.time()-now
  
  print(f"{model_name} - first prediction...")
  now=time.time()
  prediction = model.predict(sentences)
  results["first_prediction_seconds"]=time.time()-now
  
  print(f"{model_name} - second prediction...")
  now=time.time()
  prediction = model.predict(sentences)
  results["second_prediction_seconds"]=time.time()-now

  results["embedding_size"]=prediction.shape[1]
  results["additional_infos"]=json.dumps(model.additional_infos())

  return results


def safe_benchmark_prediction_model(model_name, sentences, results=None):
  if results is None:
    results={}

  try:
    benchmark_prediction_model(model_name, sentences, results)
    results["success"]=True
  except:
    results["success"]=False

  return results


class BenchmarkingTools():
  def __init__(self):
    self.manager = multiprocessing.Manager()

  def benchmark_and_cleanup(self, model_name, sentences):
    """
      tests model performances in a separate process
      when the process dies, python should purge 
      occupied resources such as RAM and GPU memory
      Source:
      https://github.com/tensorflow/tensorflow/issues/36465
    """
    return_dict = self.manager.dict() # source: https://stackoverflow.com/questions/10415028/how-can-i-recover-the-return-value-of-a-function-passed-to-multiprocessing-proce
    process_eval = multiprocessing.Process(
        target=safe_benchmark_prediction_model, args=(model_name, sentences, return_dict))
    process_eval.start()
    process_eval.join()
    return dict(return_dict)

prediction_models=['talkheads_ggelu_bert_en_large',
 'bert_en_uncased_L12_H768_A12',
 'small_bert_en_uncased_L4_H512_A8',
 'bert_en_uncased_L2_H128_A2',
 'bert_en_uncased_L24_H1024_A16',
 'bert_en_cased_L12_H768_A12',
 'bert_en_uncased_L2_H512_A8',
 'bert_en_uncased_L4_H128_A2',
 'bert_en_uncased_L2_H768_A12',
 'bert_en_uncased_L2_H256_A4',
 'lambert_en_uncased_L24_H1024_A16',
 'small_bert_en_uncased_L12_H768_A12',
 'bert_en_uncased_L4_H256_A4',
 'bert_en_uncased_L4_H768_A12',
 'bert_en_uncased_L8_H512_A8',
 'bert_en_cased_L24_H1024_A16',
 'bert_en_wwm_cased_L24_H1024_A16',
 'bert_en_uncased_L8_H256_A4',
 'bert_en_uncased_L6_H256_A4',
 'bert_en_uncased_L12_H512_A8',
 'bert_en_uncased_L8_H128_A2',
 'bert_en_wwm_uncased_L24_H1024_A16',
 'bert_en_uncased_L12_H256_A4',
 'talkheads_ggelu_bert_en_base',
 'bert_en_uncased_L8_H768_A12',
 'bert_en_uncased_L6_H768_A12',
 'bert_en_uncased_L6_H512_A8',
 'bert_en_uncased_L6_H128_A2',
 'bert_en_uncased_L12_H128_A2',
 'bert_en_uncased_L10_H768_A12',
 'bert_en_uncased_L10_H512_A8',
 'bert_en_uncased_L10_H256_A4',
 'bert_en_uncased_L10_H128_A2',
 'bert_wiki_books',
 'bert_wiki_books_stt2',
 'bert_wiki_books_squad2',
 'bert_wiki_books_qqp',
 'bert_wiki_books_qnli',
 'bert_wiki_books_mnli',
 'UniversalSentenceEncoderCmlmEnBase',
 'UniversalSentenceEncoderCmlmMultilingualBaseBr',
 'UniversalSentenceEncoderCmlmMultilingualBase',
 'UniversalSentenceEncoderCmlm',
 'UniversalSentenceEncoder',
 'UniversalSentenceEncoderMultilingual',
 'UniversalSentenceEncoderLarge',
 'UniversalSentenceEncoderMultilingualLarge',
 'NnlmEnDim128',
 'NnlmEnDim128WithNormalization',
 'NnlmEnDim50',
 'NnlmEnDim50WithNormalization',
 'GnewsSwivel20dim',
 'WikiWords250',
 'WikiWords250WithNormalization',
 'WikiWords500',
 'WikiWords500WithNormalization']

sentences=[
"Give me a bright guitar",
"I'd like a sharp cello",
"give me a dry acoustic guitar",
"give me a metallic harp",
"give me a dirty organ",
"give me a hollow piano",
"give me a sharp trumpet",
"give me a cold triangle",
"give me dark drums",
"give me a soft french horn",
"give me a dull clarinet",
"give me a smooth operator",
"Give me a simple square bass",
"Give me an orchestral string",
"Give me an analog pad",
"Give me a simple sine bass",
"Give me a chord preset",
"Get me a 909 closed hi-hat",
"Get me an 808 open hi-hat",
"Give me a round bass",
"Give me a sharp synth",
"Give me a warm pad",
"Give me a wide stereo pad",
"Give me a mono, warm, round synth bass",
"Make me a soft flute that sounds like a chirping bird ",
"Give me a dark brassy sound",
"Can you give me a wailing guitar?",
"Get me a scratchy violin",
"Give me a Star Wars laser beam sound",
"Can you combine a low piano sound with a roaring lion?",
"Get me something like a compact bleep",
"Give me a funky guitar"
 ]

if __name__=='__main__':
    #sentences=["a","abababa","gkj"]
    #prediction_models=["talkheads_ggelu_bert_en_large", "UniversalSentenceEncoderMultilingual"]
    
    
    tools=BenchmarkingTools()
    results = []
    for p in tqdm(prediction_models):
      r=tools.benchmark_and_cleanup(p, sentences)
      #r=benchmark_prediction_model(p, sentences)
      results.append(r)
    
    df=pd.DataFrame(results)
    df.to_csv("results.csv", index=False)
    df

    from google.colab import files
    files.download( "results.csv" )

