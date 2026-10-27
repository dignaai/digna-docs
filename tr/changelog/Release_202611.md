# Sürüm Notları – 2026.11  

Sürüm 2026.11 üç önemli yenilik etrafında şekilleniyor:

- **digna Data Reconciliation**: verilerin sistemler arasında taşınırken tutarlı kalıp kalmadığını kontrol eder  
- **digna Agentic**: digna MCP Server aracılığıyla digna'yı AI ajanlarına açar  
- **digna Engine**: isteğe bağlı olarak verileri digna içinde profiller ve farklı veritabanı teknolojileri arasında referans bütünlüğü kontrollerini mümkün kılar  

digna Data Reconciliation ve digna Agentic beta sürüm olarak sunulmaktadır.

---

## Yeni Özellikler  

### digna Data Reconciliation – Kaynaktan Hedefe Tutarlılık  
Veriler bir rapora ulaşmadan önce çoğu zaman birkaç sistemden geçer. digna Data Reconciliation, bir **hedef** veri kaynağını onu oluşturan **kaynaklarla** karşılaştırır ve artık eşleşmediklerinde alarm verir.

- Hedef veri kaynağının yeni **Data Reconciliation** sekmesinde adlandırılmış kurallar olarak yapılandırılır  
- Projede Data Reconciliation özelliği açık olan her veri kaynağı bir kaynak olabilir  
- Kullanım alanları arasında standart mutabakat prosedürleri ve ETL süreçlerinin sonuçlarının doğrulanması yer alır  
- İki kural türü: **Exact** ve **AI**  

**Exact Kuralları – Veri Kalitesi Kuralı Olarak Mutabakat**: Bir kaynak ile bir hedef arasında tam olarak neyin eşleşmesi gerektiğini, tıpkı bir veri kalitesi kuralında olduğu gibi siz tanımlarsınız.

  - Bir kaynak veri kaynağını bir hedef veri kaynağıyla karşılaştırma  
  - Bir hedef kontrolünü, istatistik ve özniteliğe göre bir kaynak kontrolüyle eşleştirme, ör. satır sayıları veya bir tutar sütununun toplamı  
  - Farka **absolute** bir toleransla (ör. ± 10) veya **relative** bir toleransla (ör. kaynağın ± %0,5'i) izin verme  
  - Zaman çizelgesi her günün farkını toleransa göre gösterir  

**AI Kuralları – Veri Gözlemlenebilirliği Olarak Mutabakat**: digna, diğer modüllerde verileri gözlemlediği şekilde bir hedefin kaynaklarını nasıl takip ettiğini öğrenir ve bu ilişki bozulduğunda alarm verir.

  - Birden fazla kaynak veri kaynağının kontrollerini tek bir hedefin kontrolleriyle birleştirme  
  - Aralarındaki mantığı (join'ler, filtreler, toplulaştırmalar) bilmeniz veya yazmanız gerekmez  
  - Bir model, hedefin aynı gündeki kaynaklarını nasıl takip ettiğini geçmiş verilerden öğrenir  
  - Her hedef kontrolü o günün kaynak değerlerinden tahmin edilir ve hedef, kuralın kendi geçmiş hatalarından oluşan bandın dışına çıktığında digna alarm verir  
  - Her kuralın kendi **Model settings** ayarları vardır: **Sensitivity**, **Memory** ve **Model Complexity**  

Mutabakat kontrolleri Dashboard'da kural başına bir zaman çizelgesiyle görünür. Genel inceleme durumuna dahil edilir ve bildirimleri tetikler.

**Etkisi:** Mutabakatın her iki tarafını da kapsar. Exact kurallar kaynak ile hedef arasındaki bilinen kontrolleri uygular, AI kurallar ise ETL süreçleri gibi karmaşık akışları izler; böylece yolda kaybolan veya değişen veriler, elle yazılmış mutabakat SQL'ine gerek kalmadan yakalanır.

---

### digna Agentic – AI Ajanları için digna  
digna Agentic'in ilk sürümü. AI ajanları artık digna ile çalışabilir, verileriniz hakkındaki iş sorularını yanıtlayabilir ve yapılandırmanızı iyileştirmenize yardımcı olabilir.

**digna MCP Server**: Claude ve diğer AI ajanlarının Model Context Protocol aracılığıyla digna ile çalışmasını sağlar.

  - Projeleri, veri kaynaklarını, kuralları, inceleme zamanlamalarını ve abonelikleri yönetme  
  - Uyarıları araştırmak için inceleme durumlarını tek tek kontrollere kadar okuma  

**Veri Kaynakları ve Öznitelikler için Açıklamalar**: Bir veri kaynağının veya özniteliğin ne içerdiğini sade bir dille açıklayın.

  - AI ajanları verilerinizi yorumlamak için bu açıklamaları kullanır  
  - Verileriniz hakkında iş soruları sorun; AI ajanları bunları digna'nın izlediği verilerden yanıtlar  
  - digna'nın mevcut yapılandırması bir soruyu yanıtlayamıyorsa, AI ajanı mümkün olduğunda veri kaynağında ve özniteliklerinde değişiklikler önerir, ör. yeni bir veri seti eklenmesi  

**Etkisi:** Verileriniz hakkında sade bir dille iş soruları sormanızı sağlar ve AI ajanlarının digna'yı yapılandırmanıza ve veri kalitesi sorunlarını araştırmanıza yardımcı olmasına olanak tanır.

---

### digna Engine – Profillemeyi Seçtiğiniz Yerde Yapın  
Varsayılan olarak digna, verileri bulundukları yerde, yani kaynak veritabanında profiller. digna Engine yeni bir seçenek ekler: digna verileri kaynaktan dışa aktarır ve digna Engine içinde profiller.

- Zorunlu değil, isteğe bağlı: kaynak veritabanında profilleme kullanılmaya devam edebilir  
- Her veritabanı bağlantısı için **profilleme konumu** olarak seçilir: **Source Database** veya **digna Engine**  
- Desteklenen tüm kaynak teknolojileri için kullanılabilir  

**Bağlantılar Arası Referans Bütünlüğü**: Bazı kontroller verilerin dışa aktarılmasını gerektirir. digna Engine, bu durumlar için **digna Data Validation**'ı genişletir.

  - **Farklı veritabanı bağlantılarındaki** veri kaynakları arasında, farklı veritabanı teknolojileri de dahil olmak üzere (ör. Oracle ve PostgreSQL) **Referans Bütünlüğü Kontrolleri**  
  - Her iki profilleme konumuyla da çalışır: Source Database için yalnızca anahtar sütunlar digna Engine'e aktarılır  
  - Dashboard, bir kontrolün iki bağlantı arasında çalıştığını gösterir  

**Etkisi:** Verilerin nerede profilleneceğini seçmenizi sağlar ve farklı veritabanı teknolojileri üzerinde çalışan sistemler arasındaki ilişkileri uygular.

---

## Profilleme Geliştirmeleri  

Bu sürüm ayrıca kullanıcılara neyin ve nasıl profilleneceği üzerinde daha fazla kontrol sağlar.

### Sorgu Öznitelikleri – Kullanıcı Tanımlı Sütunlar  
- Yapay sütunlar tanımlayın: veri kaynağının bir veya daha fazla sütunu üzerinde bir SQL ifadesi  
- Her sorgu özniteliğinin kendi adı vardır  
- Diğer tüm öznitelikler gibi profillenir ve kontrol edilir  

### DATE Sütun Kategorisi  
- Öznitelikler için yeni **Date** kategorisi  
- İncelenen tarihe göreli metrikler  

### İsteğe Bağlı Profilleme  
- Bir inceleme çalıştırmadan, herhangi bir özniteliği tek bir tarihin tam anlık görüntüsü üzerinde profilleyin  
- Özniteliğin sütun türünü belirlemeye yardımcı olur: **Numerical**, **Categorical**, **Date** veya **Unspecified**  

---

## Bu Sürümden Kim Yararlanır  

- **Veri Mühendisleri:** digna Data Reconciliation ile ETL sonuçlarının doğrulanması  
- **Finans, Risk ve Controlling Ekipleri:** digna Data Reconciliation içinde Exact kurallar olarak standart mutabakat prosedürleri  
- **Veri Kalitesi ve Yönetişim Ekipleri:** digna Engine ile veritabanı teknolojileri arasında referans bütünlüğü  
- **İş Kullanıcıları:** digna Agentic ile AI ajanları tarafından yanıtlanan, verilerle ilgili iş soruları  
- **AI ve Otomasyon Ekipleri:** digna Agentic aracılığıyla digna ile çalışan AI ajanları  

---

## CLI Güncellemeleri  
- Değişiklik yok  

---