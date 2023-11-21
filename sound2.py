import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# 音階（C、C#、D、...、B）のリスト
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# 基準となるA4の周波数
A4 = 440
# A4からの半音の数を計算
note_freqs = {note: (A4 * 2 ** ((i - 9) / 12)) for i, note in enumerate(notes)}

# 関数定義: 周波数から音階を取得
def get_note_name(frequency):
    # 最も近い半音の周波数を見つける
    half_steps = round(12 * np.log2(frequency/A4))
    # 周波数から音階を計算
    note_index = half_steps % 12
    octave = (half_steps + 9) // 12
    return notes[note_index] + str(octave)

# PyAudioのインスタンスを生成
p = pyaudio.PyAudio()

# オーディオストリームを開く
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=2048)

print("* 録音開始")

# matplotlibの設定
plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1)

# フレームを読み込んで、ストリームを処理する
for i in range(0, int(44100 / 2048 * 5)):
    data = np.frombuffer(stream.read(2048), dtype=np.int16)
    
    # 波形のプロット
    ax1.clear()
    ax1.plot(data)
    ax1.set_title("Input Sound Wave")
    ax1.set_ylim([-2**15, (2**15)-1])
    ax1.set_xlim([0, 2048])

    # 周波数成分の計算
    fft_data = np.abs(np.fft.fft(data))
    fft_data = fft_data[:int(len(fft_data)/2)]
    
    xf = np.linspace(0, 44100 / 2, len(fft_data))

    # 周波数のプロット
    ax2.clear()
    ax2.semilogx(xf, fft_data)
    ax2.set_title("Frequencies")
    ax2.set_xlim([20, 44100 / 2])
    
    # ピークの検出
    peaks, _ = find_peaks(fft_data, height=200)
    peak_freq = xf[peaks]
    peak_db = fft_data[peaks]
    
    # 最も高いピーク（最も基本と思われる周波数）を見つける
    if peaks.size > 0:
        fundamental_freq = peak_freq[np.argmax(peak_db)]
        note_name = get_note_name(fundamental_freq)
        print(f"基本周波数: {fundamental_freq} Hz, 音階: {note_name}")
    else:
        print("ピークなし")

    plt.pause(0.01)

print("* 録音終了")

# ストリームを閉じる
stream.stop_stream()
stream.close()
p.terminate()
plt.ioff()
plt.show()
