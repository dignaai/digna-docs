# Gemini'yi digna'ya Bağlayın

Bu kılavuz, Google'ın Gemini araçlarını **digna MCP Server**'a bağlar.
[AI Ajanlarına Genel Bakış](overview.md) sayfasında açıklandığı gibi, *digna* kurulumunuzun MCP
uç noktasına ve bir API anahtarına ihtiyacınız vardır.

Örneklerde uç nokta olarak `https://digna.example.com/mcp` kullanılmıştır. Bunu kendi uç
noktanızla değiştirin.

## Aracınızı Seçin {: #choose-your-tool }

| Araç | Kimin için | Yapılandırma |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE ve uygulama | Google'ın ajan araçları. Antigravity CLI, Haziran 2026'da bireysel Google hesapları için Gemini CLI'ın yerini aldı | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Gemini Code Assist Standard ve Enterprise lisansları ile ücretli Gemini API anahtarları | `settings.json` veya `gemini mcp add` |
| Gemini Enterprise uygulaması | — | Desteklenmez. Özel MCP bağlayıcısı OAuth veya bir Google Cloud hizmet hesabıyla oturum açarken digna MCP Server API anahtarlarıyla kimlik doğrulaması yapar |

Bu araçların tümü üzerinde çalıştıkları makineden bağlanır; bu nedenle o makine uç noktaya
ulaşabildiği sürece şirket ağınızın içindeki *digna* ile çalışırlar.

---

## Antigravity {: #antigravity }

Antigravity, MCP sunucularını CLI, IDE ve uygulama tarafından paylaşılan `mcp_config.json`
dosyasından okur.

### 1. mcp_config.json Dosyasını Açın {: #1-open-mcp-config-json }

| Kapsam | Dosya |
|---|---|
| Tüm projeleriniz | `~/.gemini/config/mcp_config.json` |
| Tek bir çalışma alanı | Çalışma alanındaki `.agents/mcp_config.json` |

Kullanılan dosyayı açmak için:

- **CLI**: MCP yöneticisini açmak için `/mcp` yazın ve ++enter++ tuşuna basın.
- **IDE**: ajan yan panelinde **…** menüsünü açın, **MCP Servers**'ı, ardından
  **Manage MCP Servers**'ı, ardından **View raw config**'i seçin.
- **Uygulama**: **Customizations** > **Installed** > **MCP Servers** bölümüne gidin ve
  **Copy Config File Path** seçeneğini kullanın.

### 2. digna Sunucusunu Ekleyin {: #2-add-the-digna-server }

`digna` girişini ekleyin. Dosyada zaten bir `mcpServers` bölümü varsa, onu oraya ekleyin:

```json
{
  "mcpServers": {
    "digna": {
      "serverUrl": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <api key>"
      }
    }
  }
}
```

Antigravity uzak sunuculara yalnızca digna MCP Server'ın kullandığı streamable HTTP üzerinden
ulaşır. Uç noktayı `serverUrl` olarak yazın; Gemini CLI'ın `httpUrl` anahtarı desteklenmez.

### 3. Bağlantıyı Doğrulayın {: #3-verify-the-connection }

CLI'da `/mcp` yazın: MCP yöneticisi `digna` sunucusunu durumu ve araçlarıyla birlikte gösterir,
ayrıca yapılandırmayı yeniden yükleyebilir ve bağlantı günlüklerini gösterebilir. IDE'de sunucu
**Manage MCP Servers** altında görünür.

!!! warning "Dosyayı Koruyun"

    `mcp_config.json`, API anahtarını düz metin olarak tutar. Çalışma alanındaki
    `.agents/mcp_config.json` dosyasını sürüm kontrolünün dışında tutun ve genel dosyayı yalnızca
    kendi hesabınızın okuyabilmesini sağlayın.

---

## Gemini CLI {: #gemini-cli }

### 1. Sunucuyu Ekleyin {: #1-add-the-server }

API anahtarını bir ortam değişkenine koyun, ardından sunucuyu ekleyin:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

Komutu çalıştırdığınızda kabuğunuz `$DIGNA_API_KEY` değerini yerine koyar, böylece Gemini CLI
anahtarı kendi ayarlarında saklar. `--scope user` olmadan sunucu yalnızca geçerli projeye eklenir.

### 2. Veya settings.json Dosyasını Düzenleyin {: #2-or-edit-settings-json }

Yukarıdaki komut `settings.json` dosyasına yazar. Dosyayı kendiniz düzenlemek için:

| Kapsam | Dosya |
|---|---|
| Tüm projeleriniz | `~/.gemini/settings.json` |
| Tek bir proje | Projedeki `.gemini/settings.json` |

```json
{
  "mcpServers": {
    "digna": {
      "httpUrl": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <api key>"
      }
    }
  }
}
```

Streamable HTTP için anahtar olan `httpUrl`'yi kullanın. Benzer `url` anahtarı, digna MCP
Server'ın sunmadığı eski SSE aktarımını seçer. Sunucu adında alt çizgi kullanmayın.

!!! tip "Trust'ı Kapalı Bırakın"

    Sunucuda `"trust": true` yoksa Gemini CLI her araç çağrısından önce sorar. *digna* için
    `trust`'ı kapalı bırakın, böylece bir ajanın yapılandırmanızda yaptığı her değişikliği siz
    onaylarsınız.

### 3. Bağlantıyı Doğrulayın {: #3-verify-the-connection-gemini-cli }

Kabuğunuzdan:

```bash
gemini mcp list
```

`digna` sunucusu bağlı olarak görünmelidir. Bir Gemini CLI oturumunun içinde, sunucuyu ve
araçlarını görmek için `/mcp` komutunu çalıştırın.

---

## Gemini Sorunlarını Giderme {: #troubleshooting-gemini }

### Sunucu Bağlantısız Görünüyor

- Uç noktanın `/mcp` ile bittiğini ve makinenizden erişilebilir olduğunu kontrol edin.
- Anahtar adını kontrol edin: Antigravity'de `serverUrl`, Gemini CLI'da `httpUrl`.
- `401`, anahtarın reddedildiği anlamına gelir; bkz. [401 Unauthorized](overview.md#troubleshooting).

### Gemini CLI Hesabım İçin Artık Başlamıyor

Haziran 2026'dan bu yana bireysel Google hesapları Gemini CLI yerine Antigravity CLI kullanır.
`digna` girişini [Antigravity](#antigravity) bölümünde açıklandığı gibi `mcp_config.json`
dosyasına taşıyın ve `httpUrl`'yi `serverUrl` olarak yeniden adlandırın.

---

## Ayrıca Bakınız {: #see-also }

- [AI Ajanlarına Genel Bakış](overview.md): uç nokta, API anahtarı, güvenlik ve genel sorun giderme
- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop veya bir özel bağlayıcı bağlayın
- [digna Agentic](../platform/agentic/Introduction.md): AI ajanlarının *digna* ile neler yapabildiği