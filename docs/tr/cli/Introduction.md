## Komut Satırı Arayüzü (CLI) Amacı

***digna*** Komut Satırı Arayüzü (CLI), ***digna*** platformuyla etkileşimleri kolaylaştırmak için tasarlanmış güçlü bir araçtır. Grafiksel bir kullanıcı arayüzüne ihtiyaç duymadan, kullanıcıların çok çeşitli görevleri verimli bir şekilde gerçekleştirmesine olanak tanıyan metin tabanlı bir arayüz sağlar.

### Temel Özellikler:

- **Verimlilik ve Esneklik:** CLI, komutların hızlı yürütülmesini sağlayarak üretkenliği artırır.
- **Otomasyon:** Tekrarlayan görevleri otomatikleştirmek için scripting desteği sunar.
- **Uzak Erişim:** ***digna*** kaynaklarını her yerden yönetme imkânı sağlar.
- **Tutarlılık ve Güvenilirlik:** Belgelenmiş, sürüm kontrollü komutlarla güvenilir işlemler sağlar.
- **Ölçeklenebilirlik:** Kurumsal görevler için büyük ölçekli işlemleri yönetir.
- **Öğrenme ve Ustalık:** ***digna***'nın işlevselliğini daha derinlemesine anlamayı sağlar.
- **Diğer Araçlarla Entegrasyon:** Control-M, UC4, AutomateNOW! gibi otomasyon araçlarıyla sorunsuz entegrasyon sağlar.

---

## Windows için Kurulum Talimatları

Başlamak için, gerekli dosyaları çıkarmak, *dignacli* klasörünü dağıtmak ve ***digna*** repository'sine bağlantınızı yapılandırmak için aşağıda belirtilen adımları izleyin. Başlamadan önce repository kimlik bilgilerinizi ve gerekli yapılandırma ayrıntılarını hazır bulundurun.

1. *****digna*** CLI'nin Çıkarılması:**
   - ***digna*** CLI içeren `.zip` dosyasını edinin.
   - Dosyayı istediğiniz dizine çıkarın.

2. **`dignacli` Klasörünü Dağıtma:**
   - `dignacli` klasörünü tercih ettiğiniz kurulum konumuna kopyalayın (ör. `C:\Program Files\***digna***`).

3. **`config.toml` Dosyasını Yapılandırma:**
   - `dignacli` içinde `config.toml` dosyasını kontrol edin.
   - Gerekirse `config_template.toml` dosyasının adını `config.toml` olarak değiştirin ve sağlanan dokümantasyona göre yapılandırın.