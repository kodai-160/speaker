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
while True:
	try:
		## ストリームからデータを取得
		audio_data=stream.read(BUFFER_SIZE)
		data=np.frombuffer(audio_data,dtype='int16')
		
		## リアルタイム音声波形プロット
		data_buffer = np.append(data_buffer[BUFFER_SIZE:],data)
		plt.plot(data_buffer)
		plt.ylim(-10000,10000)
		plt.draw()
		plt.pause(0.0001)
		plt.cla()
		
	except KeyboardInterrupt: ## ctrl+c で終了
		break

## 後始末
stream.stop_stream()
stream.close()
audio.terminate()