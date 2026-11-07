---
title: AI Ajanları – MCP Entegrasyonuna Genel Bakış | digna Dokümantasyonu
description: Claude, Gemini ve diğer AI ajanlarını digna MCP Server üzerinden digna'ya bağlayın. MCP uç noktasını bulun, bir API anahtarı oluşturun, lisans ve ağ gereksinimlerini kontrol edin ve AI istemcinize uygun kılavuzu seçin.
image: /assets/logo_square.png
keywords: digna MCP server, Model Context Protocol, AI ajanı bağlama, Claude MCP, Gemini MCP, Antigravity MCP, digna API anahtarı, digna Agentic
---

# AI Ajanlarını digna'ya Bağlayın

**digna MCP Server**, AI ajanlarının Claude, Gemini ve diğer birçok AI aracı tarafından desteklenen
açık bir standart olan [Model Context Protocol](https://modelcontextprotocol.io) (MCP) aracılığıyla
*digna* ile çalışmasını sağlar. *digna*'ya bağlı bir ajan, verilerinizle ilgili soruları
yanıtlayabilir, uyarıları inceleyebilir ve *digna*'nın yapılandırılmasına yardımcı olabilir.
Ajanların neler yapabildiğini görmek için [digna Agentic](../platform/agentic/Introduction.md)
sayfasına bakın.

Bu sayfa, her AI istemcisi için aynı olan *digna* tarafını ele alır. İstemci kılavuzları ise uç
noktanın ve anahtarın nereye girileceğini gösterir:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop ve özel bağlayıcılar
- [Gemini](gemini_mcp_guide.md): Antigravity ve Gemini CLI

!!! info "Beta"

    digna Agentic ve onunla birlikte digna MCP Server,
    [Release 2026.11](../changelog/Release_202611.md) ile beta sürüm olarak sunulmaktadır.

---

## Başlamadan Önce {: #before-you-start }

Şunlara ihtiyacınız var:

- *digna* Release 2026.11 veya üzeri
- **digna Agentic** içeren bir lisans. Bu olmadan MCP sunucusu her isteği reddeder
- Bir *digna* kullanıcı hesabı. Ajan, her projede bu kullanıcının izinleriyle çalışır, bkz.
  [İzinler](../platform/agentic/how_it_works.md#permissions)
- Uzak MCP sunucularına **streamable HTTP** üzerinden bağlanan ve bir `Authorization` başlığı
  gönderebilen bir AI istemcisi

---

## 1. MCP Uç Noktasını Bulun {: #1-find-the-mcp-endpoint }

MCP sunucusu *digna* arka ucunun bir parçasıdır, bu nedenle ek olarak kurulacak veya başlatılacak
bir şey yoktur. Uç noktası, arka ucun adresine `/mcp` eklenerek elde edilir:

```text
https://digna.example.com/mcp
```

Arka uç doğrudan bir ana bilgisayar ve port üzerinde çalışıyorsa, örneğin
`digna serve --address 0.0.0.0 --port 8082` komutundan sonra, uç nokta bu adrese `/mcp`
eklenmiş halidir:

```text
http://digna-host:8082/mcp
```

Arka ucun önünde bir ters proxy varsa, `/mcp` yolunu `Authorization` başlığıyla birlikte arka uca
iletmelidir.

!!! warning "Ağ Üzerinde HTTPS Kullanın"

    Her istek bir API anahtarı taşır. AI istemcisi ile *digna* aynı makinede değilse her zaman
    HTTPS kullanın.

### Bağlantı Nereden Gelir {: #where-the-connection-comes-from }

Çoğu AI istemcisi, üzerinde çalıştığı makineden bağlanır: Claude Code, yerel köprülü Claude
Desktop, Antigravity ve Gemini CLI. Bunlar için *digna*'nın yalnızca o makineden erişilebilir
olması yeterlidir, örneğin şirket ağınızın içinden.

Claude'un **özel bağlayıcıları** (custom connectors) farklıdır: uç noktaya Anthropic'in bulutu
bağlanır. Bu nedenle yalnızca uç nokta internetten HTTPS üzerinden erişilebilir olduğunda
çalışırlar. Yalnızca ağınızın içinden erişilebilen bir *digna* kurulumu için, kendi makinenizde
çalışan bir istemci kullanın.

---

## 2. Bir API Anahtarı Oluşturun {: #2-create-an-api-key }

Bir AI istemcisi, bir *digna* kullanıcısının API anahtarıyla kimlik doğrulaması yapar.

1. *digna*'da oturum açın.
2. Sol alt köşedeki kullanıcı profilinizi açın.
3. **API Keys**'e, ardından **Add API Key**'e tıklayın.
4. Anahtarın ne için olduğunu belirten bir ad girin, örn. *Claude Code – Marcin*, ve ne zaman
   sona ereceğini seçin.
5. Anahtarı kopyalayın. Yalnızca bir kez gösterilir.

MCP sunucusuna yapılan her istek, anahtarı şu başlıkta gönderir:

```text
Authorization: Bearer <api key>
```

`Bearer` kelimesi ve ondan sonraki boşluk, başlık değerinin bir parçasıdır.

---

## 3. AI İstemcinizi Bağlayın {: #3-connect-your-ai-client }

| AI istemcisi | Bağlandığı yer | Kılavuz |
|---|---|---|
| Claude Code | Kendi makineniz | [Claude](claude_mcp_guide.md#claude-code) |
| Yerel köprülü Claude Desktop | Kendi makineniz | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Claude özel bağlayıcısı (claude.ai, Claude Desktop, Claude mobil) | Anthropic'in bulutu | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE ve uygulama | Kendi makineniz | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | Kendi makineniz | [Gemini](gemini_mcp_guide.md#gemini-cli) |

Özel bir başlıkla streamable HTTP üzerinden uzak sunucuları destekleyen diğer MCP istemcileri de
çalışır. Bunların çoğu buna benzer bir yapılandırma okur. Tam dosya ve anahtar adları için
istemcinizin dokümantasyonuna bakın:

```json
{
  "mcpServers": {
    "digna": {
      "type": "http",
      "url": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <api key>"
      }
    }
  }
}
```

---

## 4. Deneyin {: #4-try-it }

Ajana yalnızca *digna*'nın yanıtlayabileceği bir şey sorun:

- *"digna projelerimi listele."*
- *"X projesindeki hangi veri kaynakları bugün yeşil değil?"*
- *"Y veri kaynağının en son başarısız kontrolünü açıkla."*

Ajan projelerinizi listelerse bağlantı çalışıyordur.

---

## Güvenlik {: #security }

- **Kişi ve istemci başına bir anahtar.** Böylece başka kimseyi etkilemeden tek bir anahtarı
  **Delete API Key** ile iptal edebilirsiniz.
- **Kullanıcıyı bilinçli seçin.** Ajan, anahtarın kullanıcısının yapabildiği her şeyi yapabilir.
  Yalnızca verileri incelemek için projelerde okuyucu rolüne sahip bir kullanıcı kullanın.
- **Anahtarları paylaşılan dosyalardan uzak tutun.** Anahtar içeren bir yapılandırma dosyasını
  commit etmeyin. İstemci destekliyorsa anahtarı bir ortam değişkeninden okuyun.
- **Bir son kullanma tarihi belirleyin.** Eski anahtarın süresi dolmadan yeni bir anahtar
  oluşturun ve istemciyi güncelleyin.
- **Araç çağrılarını gözden geçirin.** İstemcinin araç çağrıları için onay özelliğini, en azından
  yapılandırmayı değiştiren çağrılar için açık tutun.

---

## Sorun Giderme {: #troubleshooting }

### 401 Unauthorized

Yanıt nedenini belirtir:

| Mesaj | Neden |
|---|---|
| `Missing or malformed Authorization header` | Hiç başlık gönderilmedi veya değer `Bearer ` ile başlamıyor |
| `Invalid API key` | Anahtar yanlış veya silinmiş |
| `API key expired` | Anahtarın süresi dolmuş. Yeni bir anahtar oluşturun |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

*digna* lisansında digna Agentic girişi yok veya bu girişin süresi dolmuş. digna ekibinden digna
Agentic içeren bir lisans isteyin ve bunu işletim sisteminize ait kurulum kılavuzunda anlatıldığı
şekilde kurun.

### Her İstek Geçersiz Lisans Hatasıyla Başarısız Oluyor

*digna* lisansının kendisinin süresi dolmuş. MCP sunucusu, yeni bir lisans kurulana kadar
dashboard ile birlikte yanıt vermeyi durdurur.

### Ajan Okuyabiliyor Ancak Yapılandırmayı Değiştiremiyor

API anahtarının arkasındaki kullanıcı, o projede editör rolüne sahip değil. Editör rolüne sahip
bir kullanıcının anahtarını kullanın veya bir proje yöneticisinden rolü değiştirmesini isteyin.

### İstemci Hiç Bağlanamıyor

Bağlanan makine uç noktaya ulaşamıyor. Uç noktanın adresini o makineden açın ve güvenlik
duvarlarını, proxy'leri ve sertifikayı kontrol edin. Bir Claude özel bağlayıcısı için bu makine
Anthropic'in bulutundadır, bkz. [Bağlantı Nereden Gelir](#where-the-connection-comes-from).
