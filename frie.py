import matplotlib.pyplot as plt
import pyaudio as pa
import numpy as np

RATE=44100
BUFFER_SIZE=16384

## ストリーム準備
audio = pa.PyAudio()
stream = audio.open( rate=RATE,
		channels=1,
		format=pa.paInt16,
		input=True,
		frames_per_buffer=BUFFER_SIZE)

## 波形プロット用のバッファ
data_buffer = np.zeros(BUFFER_SIZE*16, int)

## 二つのプロットを並べて描画
fig  = plt.figure()
fft_fig = fig.add_subplot(2,1,1)
wave_fig = fig.add_subplot(2,1,2)

while True:
	try:
		## ストリームからデータを取得
		audio_data=stream.read(BUFFER_SIZE)
		data=np.frombuffer(audio_data,dtype='int16')
		fft_data = np.fft.fft(data)
		freq=np.fft.fftfreq(BUFFER_SIZE, d=1/RATE)
		
		## プロット
		data_buffer = np.append(data_buffer[BUFFER_SIZE:],data)
		wave_fig.plot(data_buffer)
		fft_fig.plot(freq[:BUFFER_SIZE//20],np.abs(fft_data[:BUFFER_SIZE//20]))
		wave_fig.set_ylim(-10000,10000)
		plt.pause(0.0001)
		fft_fig.cla()
		wave_fig.cla()

		
	except KeyboardInterrupt: ## ctrl+c で終了
		break

## 後始末
stream.stop_stream()
stream.close()
audio.terminate()