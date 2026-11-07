---
title: Claude – Claude'u MCP ile digna'ya Bağlama | digna Dokümantasyonu
description: Claude'u digna MCP Server üzerinden digna'ya bağlayın — komut satırından veya paylaşılan bir .mcp.json ile Claude Code, yerel köprülü Claude Desktop ve claude.ai'deki özel bağlayıcılar, Authorization başlığında bir API anahtarıyla.
image: /assets/logo_square.png
keywords: Claude MCP, Claude Code MCP, Claude Desktop MCP, claude.ai özel bağlayıcı, digna MCP server, mcp-remote, Authorization Bearer, digna API anahtarı
---

# Claude'u digna'ya Bağlayın

Bu kılavuz Claude'u **digna MCP Server**'a bağlar. [AI Ajanlarına Genel Bakış](overview.md)
sayfasında açıklandığı gibi, *digna* kurulumunuzun MCP uç noktasına ve bir API anahtarına
ihtiyacınız vardır.

Örneklerde uç nokta olarak `https://digna.example.com/mcp` kullanılmıştır. Bunu kendi uç
noktanızla değiştirin.

## Bağlantı Yöntemini Seçin {: #choose-how-to-connect }

| Claude ürünü | Bağlandığı yer | Ağınızın içindeki *digna* ile çalışır |
|---|---|---|
| [Claude Code](#claude-code) | Kendi makineniz | Evet |
| [Yerel köprülü Claude Desktop](#claude-desktop-with-a-local-bridge) | Kendi makineniz | Evet |
| claude.ai, Claude Desktop ve Claude mobil uygulamalarında [özel bağlayıcı](#custom-connector) | Anthropic'in bulutu | Hayır. Uç nokta internetten erişilebilir olmalıdır |

Şirket ağınızın içinde çalışan bir *digna* kurulumu için Claude Code'u veya yerel köprülü Claude
Desktop'ı kullanın.

---

## Claude Code {: #claude-code }

### 1. Sunucuyu Ekleyin {: #1-add-the-server }

API anahtarını bir ortam değişkenine koyun, ardından sunucuyu ekleyin:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Komutu çalıştırdığınızda kabuğunuz `$DIGNA_API_KEY` değerini yerine koyar, böylece Claude Code
anahtarı kendi yapılandırmasında saklar.

`--scope`, sunucunun nerede kullanılabileceğini belirler:

| Kapsam | Kullanılabilirlik |
|---|---|
| `local` (varsayılan) | Size, yalnızca geçerli projede |
| `user` | Size, her projede |
| `project` | Projede çalışan herkese, projedeki bir `.mcp.json` dosyası aracılığıyla |

### 2. Sunucuyu Ekibinizle Paylaşın (İsteğe Bağlı) {: #2-share-the-server-with-your-team }

Bir projedeki herkese aynı sunucuyu sağlamak için proje kök dizinine bir `.mcp.json` dosyası
ekleyin. Anahtarı dosyaya yazmayın. Claude Code, `${DIGNA_API_KEY}` değerini her kişinin kendi
ortamından doldurur:

```json
{
  "mcpServers": {
    "digna": {
      "type": "http",
      "url": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${DIGNA_API_KEY}"
      }
    }
  }
}
```

Her kişi `DIGNA_API_KEY` değişkenini kendi anahtarına ayarlar. Claude Code dosyayı ilk kez
bulduğunda, içindeki sunucuların kullanılıp kullanılmayacağını sorar.

### 3. Bağlantıyı Doğrulayın {: #3-verify-the-connection }

Kabuğunuzdan:

```bash
claude mcp list
```

`digna` sunucusu `✔ Connected` göstermelidir. Bir Claude Code oturumunun içinde, sunucuyu ve
araçlarını görmek için `/mcp` komutunu çalıştırın.

---

## Yerel Köprülü Claude Desktop {: #claude-desktop-with-a-local-bridge }

Claude Desktop'ın yapılandırma dosyası, makinenizde yerel MCP sunucuları başlatır. Küçük bir köprü
olan açık kaynaklı [`mcp-remote`](https://github.com/geelen/mcp-remote) paketi orada çalışır ve
her isteği API anahtarınızla birlikte *digna* uç noktasına iletir. Köprü kendi makinenizde
çalıştığı için bu yöntem, şirket ağınızın içindeki *digna* ile de çalışır.

!!! note "Bir Topluluk Paketi"

    `mcp-remote`, Anthropic veya digna tarafından değil, kendi açık kaynak topluluğu tarafından
    sürdürülmektedir. Kullanmadan önce kuruluşunuzun buna izin verdiğini kontrol edin.

### 1. Node.js'i Kurun {: #1-install-nodejs }

Köprü, [Node.js](https://nodejs.org) 18 veya üzerini gerektirir. Claude Desktop, sisteminizde
kurulu olan Node.js sürümünü kullanır. Şununla kontrol edin:

```bash
node --version
```

### 2. Yapılandırma Dosyasını Düzenleyin {: #2-edit-the-configuration-file }

`claude_desktop_config.json` dosyasını açın:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

`digna` sunucusunu ekleyin. Dosyada zaten bir `mcpServers` bölümü varsa, `digna` girişini oraya
ekleyin:

```json
{
  "mcpServers": {
    "digna": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://digna.example.com/mcp",
        "--transport",
        "http-only",
        "--header",
        "Authorization:${AUTH_HEADER}"
      ],
      "env": {
        "AUTH_HEADER": "Bearer <api key>"
      }
    }
  }
}
```

!!! warning "Başlığı Tam Olarak Gösterildiği Gibi Bırakın"

    `Authorization:${AUTH_HEADER}` ifadesini boşluksuz yazın ve `Bearer <api key>` değerini `env`
    içine koyun. Windows'taki Claude Desktop, `args` içindeki boşlukları kaçış karakteriyle
    işlemez, bu nedenle orada bir boşluk başlığı bozar.

### 3. Claude Desktop'ı Yeniden Başlatın {: #3-restart-claude-desktop }

Claude Desktop'tan tamamen çıkın ve yeniden başlatın. Yeni bir sohbette **+**'ya tıklayın ve
**Connectors**'ı açın: `digna` listelenmiş ve açık olmalıdır.

---

## Özel Bağlayıcı {: #custom-connector }

Özel bir bağlayıcı (custom connector), herhangi bir yerel kurulum gerektirmeden *digna*'yı
claude.ai, Claude Desktop ve Claude mobil uygulamalarında kullanılabilir hale getirir. Uç noktaya
Anthropic'in bulutu bağlanır, bu nedenle bu yöntem yalnızca şu durumlarda çalışır:

- *digna* uç noktası internetten HTTPS üzerinden erişilebilir
- Claude kuruluşunuzda **Add custom connector** iletişim kutusunda **Request headers** seçeneği
  bulunuyor. Anthropic bunu sınırlı sayıda kuruluşa beta olarak sunmaktadır

!!! warning "Ağınızın İçindeki digna İçin Değil"

    Özel bir ağın içindeki sunuculara ulaşan Claude MCP tünelleri, MCP sunucusunda OAuth
    gerektirir. digna MCP Server API anahtarlarıyla kimlik doğrulaması yaptığından tünel
    kullanılamaz. Bunun yerine [Claude Code](#claude-code) veya
    [yerel köprülü Claude Desktop](#claude-desktop-with-a-local-bridge) kullanın.

### 1. Bağlayıcı Ayarlarını Açın {: #1-open-the-connector-settings }

- **Free, Pro, Max ve Ultra planları**: **Customize > Connectors** bölümüne gidin ve
  **Add custom connector**'a tıklayın.
- **Team ve Enterprise planları**: bir Owner **Organization settings > Connectors** bölümüne
  gider, **Add**'e, ardından **Custom**'a tıklar ve tür sorulursa **Web**'i seçer.

### 2. Bağlayıcı Bilgilerini Girin {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: başlık adı olarak `authorization` seçin, değer olarak `Bearer` kelimesi ve
   boşluk dahil `Bearer <api key>` girin ve **Required** olarak işaretleyin.
4. **Add**'e tıklayın.

!!! warning "Herkes Aynı Anahtarı Paylaşır"

    Bağlayıcıyı kullanan her üye aynı API anahtarıyla, dolayısıyla aynı *digna* kullanıcısıyla
    çalışır. Bağlayıcı için ayrı bir *digna* kullanıcısı oluşturun ve ona yalnızca herkesin sahip
    olabileceği projeleri ve rolleri verin, örn. okuyucu rolünü.

Team ve Enterprise planlarında üyeler daha sonra **Customize > Connectors** altından bağlanır;
burada bağlayıcı **Custom** etiketini taşır.

Claude, mevcut bir bağlayıcının başlığını değiştiremez. Yeni bir anahtar kullanmak için
bağlayıcıyı kaldırın ve yeniden ekleyin.

---

## Claude Sorunlarını Giderme {: #troubleshooting-claude }

### claude mcp list, Failed to connect Gösteriyor

Nedenini görmek için `claude mcp get digna` komutunu çalıştırın. `401`, anahtarın reddedildiği
anlamına gelir; bkz. [401 Unauthorized](overview.md#troubleshooting). Claude Code ayrıca,
anahtarı kopyalarken sıkça oluşan, anahtarın başında veya sonundaki boşluklar ya da satır sonları
konusunda da uyarır.

### digna, Claude Desktop'ta Görünmüyor

- Node.js 18 veya üzerinin kurulu olduğunu kontrol edin: `node --version`.
- `claude_desktop_config.json` dosyasının geçerli JSON olduğunu kontrol edin. Eksik bir virgül,
  dosyadaki tüm sunucuların yüklenmesini engeller.
- Claude Desktop'tan yalnızca pencereyi kapatarak değil, tamamen çıkın ve yeniden başlatın.

### Özel Bağlayıcı Sunucuya Ulaşamıyor

Anthropic'in bulutu uç noktaya ulaşamıyor. Uç noktanın internetten HTTPS üzerinden geçerli bir
sertifikayla erişilebilir olduğunu kontrol edin veya bunun yerine [Claude Code](#claude-code)
üzerinden bağlanın.

---

## Ayrıca Bakınız {: #see-also }

- [AI Ajanlarına Genel Bakış](overview.md): uç nokta, API anahtarı, güvenlik ve genel sorun giderme
- [Gemini](gemini_mcp_guide.md): Antigravity veya Gemini CLI'ı bağlayın
- [digna Agentic](../platform/agentic/Introduction.md): AI ajanlarının *digna* ile neler yapabildiği
