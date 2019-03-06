# import soundfile
import librosa
import numpy as np
from pypesq import pesq
from pystoi.stoi import stoi
import FLAGS

'''
soundfile.info(file, verbose=False)
soundfile.available_formats()
soundfile.available_subtypes(format=None)
soundfile.read(file, frames=-1, start=0, stop=None, dtype='float64', always_2d=False, fill_value=None, out=None, samplerate=None, channels=None, format=None, subtype=None, endian=None, closefd=True)
soundfile.write(file, data, samplerate, subtype=None, endian=None, format=None, closefd=True)
'''


def read_audio(file):
  data, sr = librosa.load(file)
  data = librosa.resample(data, sr, FLAGS.PARAM.FS, res_type='kaiser_fast')
  return data*32767, FLAGS.PARAM.FS


def write_audio(file, data, sr):
  data /= 32767
  return librosa.output.write(file, data, sr)


def get_batch_pesq_improvement(x_wav,y_wav,y_wav_est):
  '''
  inputs:
    x_wav, y_wav, y_wav_est: [batch,wave]
  return:
     average mixture pesq, average enhanced pesq, average pesq improvement
  '''
  # calculate PESQ improvement
  pesq_ref_cleaned_list = [pesq(ref, cleaned, FLAGS.PARAM.FS)
                           for ref, cleaned in zip(y_wav, y_wav_est)]
  pesq_ref_mixed_list = [pesq(ref, mixed, FLAGS.PARAM.FS)
                         for ref, mixed in zip(y_wav, x_wav)]
  pesq_ref_cleaned_vec = np.array(pesq_ref_cleaned_list)
  pesq_ref_mixed_vec = np.array(pesq_ref_mixed_list)
  pesq_imp_vec = pesq_ref_cleaned_vec - pesq_ref_mixed_vec
  avg_pesq_mixed = np.mean(pesq_ref_mixed_vec)
  avg_pesq_cleaned = np.mean(pesq_ref_cleaned_vec)
  avg_pesq_imp = np.mean(pesq_imp_vec)
  return {'mixture pesq': avg_pesq_mixed, 'enhanced pesq': avg_pesq_cleaned, 'pesq imp': avg_pesq_imp}


def get_batch_stoi_improvement(x_wav,y_wav,y_wav_est):
  '''
  inputs:
    x_wav, y_wav, y_wav_est: [batch,wave]
  return:
     average mixture stoi, average enhanced stoi, average stoi improvement
  '''
  # calculate STOI improvement
  stoi_ref_cleaned_list = [stoi(ref, cleaned, FLAGS.PARAM.FS)
                           for ref, cleaned in zip(y_wav, y_wav_est)]
  stoi_ref_mixed_list = [stoi(ref, mixed, FLAGS.PARAM.FS)
                         for ref, mixed in zip(y_wav, x_wav)]
  stoi_ref_cleaned_vec = np.array(stoi_ref_cleaned_list)
  stoi_ref_mixed_vec = np.array(stoi_ref_mixed_list)
  stoi_imp_vec = stoi_ref_cleaned_vec - stoi_ref_mixed_vec
  avg_stoi_mixed = np.mean(stoi_ref_mixed_vec)
  avg_stoi_cleaned = np.mean(stoi_ref_cleaned_vec)
  avg_stoi_imp = np.mean(stoi_imp_vec)
  return {'mixture stoi': avg_stoi_mixed, 'enhanced stoi': avg_stoi_cleaned, 'stoi imp': avg_stoi_imp}


def get_batch_sdr_improvement(x_wav,y_wav,y_wav_est):
  return 'waiting implement.'
