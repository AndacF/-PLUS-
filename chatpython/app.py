from flask import Flask, request, jsonify
from llama_cpp import Llama
import unicodedata

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Türkçe karakter

model_path = "C:/Users/Pelin/Desktop/ödevllm/llama3-8b/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"  

# Model
llm = Llama(model_path=model_path, n_gpu_layers=20, n_ctx=2048, n_threads=4, verbose=False)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    isim = data.get('isim', 'Bilgi Yok')
    ates = data.get('ateş', 'Bilgi Yok')
    nabiz = data.get('nabız', 'Bilgi Yok')
    tansiyon = data.get('tansiyon', 'Bilgi Yok')
    notlar = data.get('not', 'Bilgi Yok')

    # Prompt'u resmi ve kısa bir yanıt için ayarla
    prompt = f"""<|begin_of_text|><|start_header_id|>user<|end_header_id>
Sen, girdi olarak sağlanan hasta verilerini (semptomlar, vital bulgular, laboratuvar sonuçları, tıbbi geçmiş vb.) analiz eden bir tıbbi yapay zekâ asistanısın. Görevin, sağlık profesyonellerine destek olmak amacıyla, verilere dayalı olası tanıları ve aciliyet değerlendirmesini özetlemektir. Unutma, senin yanıtların kesin tıbbi tanı veya tedavi önerisi değildir ve mutlaka kalifiye bir sağlık uzmanı tarafından değerlendirilmelidir.

Yanıtını aşağıdaki katı kurallara göre oluştur:

İlk Cümle: 'Hasta [Hastanın Adı]' ile başla. Sunulan hasta verilerine ve sağlıklı verilere (standart referans değerlere) dayanarak, ayırıcı tanı listesindeki en olası ön tanıyı/tanıları açıkça belirt. (Örnek: "Hasta Ayşe Yılmaz için sunulan verilere göre en olası ön tanılar viral gastroenterit veya gıda zehirlenmesidir.")

İkinci Cümle: Belirtilerin şiddeti, olası tanı(lar) ve klinik aciliyet durumunu göz önünde bulundurarak, tek bir uygun eylem önerisi sun. Şu seçeneklerden en uygun olanını seç: "rutin poliklinik takibi uygundur", "ek tetkikler (örneğin, [test adı]) planlanmalıdır", "[uzmanlık alanı] uzmanı konsültasyonu önerilir" veya yalnızca hayatı tehdit eden durumlarda "acil tıbbi müdahale gereklidir". (Örnek: "Belirtilerin şiddeti göz önüne alındığında, ayaktan takip ve semptomatik tedavi ile poliklinik kontrolü uygundur.")

Yanıtın toplamda iki cümleyi aşmasın. Dilin profesyonel, net ve objektif olsun.

TÜM veriler normal sınırlardaysa ve anlamlı bir klinik bulgu(Notda) yoksa herhangi bir tanı ve eylem önerisinde bulunmana gerek yok.

    
Sağlıklı Veriler:
- Ateş: 36,5–37,5 °C
- Nabız: 60–100 bpm
- Tansiyon: 120/80 mmHg

Hasta Verileri:
- İsim: {isim}
- Ateş: {ates} °C 
- Nabız: {nabiz} bpm 
- Tansiyon: {tansiyon} mmHg 
- Not: {notlar}
<|eot_id|><|start_header_id|>assistant<|end_header_id>
"""

    # Modelden yanıt
    response = llm(prompt, max_tokens=200, temperature=0.5, top_p=0.90, stop=["<|eot_id|>"])
    model_evaluation = response["choices"][0]["text"].strip()

    final_response_text = unicodedata.normalize('NFC', model_evaluation)

    # JSON formatı
    return jsonify({"cevap": final_response_text}), 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == '__main__':
    app.run(port=5000)