export type LegalCategory =
  | 'MEDENİ HUKUK'
  | 'ANAYASA HUKUKU'
  | 'CEZA HUKUKU'
  | 'BORÇLAR HUKUKU'
  | 'İDARE HUKUKU';

export type LegalEntry = {
  id: string;
  category: LegalCategory;
  term: string;
  definition: string;
};

export const legalTerms: LegalEntry[] = [
  // MEDENİ HUKUK
  {
    id: 'medenihukuk-nafaka',
    category: 'MEDENİ HUKUK',
    term: 'NAFAKA',
    definition:
      'Geçimlik; yasaların belirlediği durumlarda, genellikle, zaruret içinde bulunan kimseye kanunda belirtilen yükümlüler tarafından verilmesi gerekli yardım.',
  },
  {
    id: 'medenihukuk-tasarruf',
    category: 'MEDENİ HUKUK',
    term: 'TASARRUF',
    definition:
      'Bir şeyden yararlanabilme ve o şey üzerinde istenilen hukuksal veya eylemsel işlemleri yapabilme kudreti; harcama; harcamada bulunma.',
  },
  {
    id: 'medenihukuk-gaiplik',
    category: 'MEDENİ HUKUK',
    term: 'GAİPLİK KARARI',
    definition:
      'Ölüm tehlikesi içinde yiten veya kendisinden çoktan beri haber alınamayan bir kimsenin ölümü pek olası görünürse, hakları bu ölüme bağlı olanların istemi ile yargıcın yitikliğe karar vermesi.',
  },
  {
    id: 'medenihukuk-kisilik',
    category: 'MEDENİ HUKUK',
    term: 'KİŞİLİK',
    definition:
      'Şahsiyet; kişi varlığı; kişinin maddi ve manevi varlığı; bir kimseyi, diğerinden ayıran fiziksel ve ruhsal varlık.',
  },
  {
    id: 'medenihukuk-zilyetlik',
    category: 'MEDENİ HUKUK',
    term: 'ZİLYETLİK',
    definition:
      'Bir şey üzerindeki fiili tasarruf biçiminde ortaya çıkan hâkimiyet; elmenlik.',
  },

  // ANAYASA HUKUKU
  {
    id: 'anayasa-cumhuriyet',
    category: 'ANAYASA HUKUKU',
    term: 'CUMHURİYET',
    definition:
      'Ulusun egemenliği elinde bulundurduğu ve bunu belirli sürelerle seçtiği milletvekilleri aracılığıyla kullandığı devlet biçimi.',
  },
  {
    id: 'anayasa-anayasa-mahkemesi',
    category: 'ANAYASA HUKUKU',
    term: 'ANAYASA MAHKEMESİ',
    definition:
      'Yasaların, kanun gücünde kararnamelerin ve TBMM İçtüzüğünün Anayasaya uygunluğunu denetleyen mahkeme.',
  },
  {
    id: 'anayasa-millet',
    category: 'ANAYASA HUKUKU',
    term: 'MİLLET',
    definition:
      'Devletin unsurlarından biri; kendilerini diğer toplumlardan ayrı sayan, din, dil, kültür birliğine sahip topluluk.',
  },
  {
    id: 'anayasa-devlet',
    category: 'ANAYASA HUKUKU',
    term: 'DEVLET',
    definition:
      'Halk, ülke, egemenlik ve ülkü birliği ile kurulan varlık; belirli bir sınırla çevrili toprağa ve örgütlenmiş halka sahip siyasi yapı.',
  },
  {
    id: 'anayasa-insan-haklari',
    category: 'ANAYASA HUKUKU',
    term: 'İNSAN HAKLARI',
    definition:
      'Devlet karşısında, hiçbir ayırım gözetmeksizin bireye ait eşitlik, mülkiyet, özgürlük, güvence gibi haklar.',
  },

  // CEZA HUKUKU
  {
    id: 'ceza-iskence',
    category: 'CEZA HUKUKU',
    term: 'İŞKENCE',
    definition:
      'Herhangi bir amaçla birisine maddi veya manevi büyük acı verici harekette bulunmak.',
  },
  {
    id: 'ceza-gasp',
    category: 'CEZA HUKUKU',
    term: 'GASP',
    definition:
      'Zorla alma; bir malı sahibinin rızası dışında zor kullanarak alma.',
  },
  {
    id: 'ceza-suca-istirak',
    category: 'CEZA HUKUKU',
    term: 'SUÇA İŞTİRAK',
    definition:
      'Birden çok kişinin önceden anlaşarak ortak olarak bir suçu işlemeleri.',
  },
  {
    id: 'ceza-suca-tesebbus',
    category: 'CEZA HUKUKU',
    term: 'SUÇA TEŞEBBÜS',
    definition:
      'İcra fiillerine başlanmasına rağmen suçun failin iradesi dışında tamamlanmaması durumu.',
  },
  {
    id: 'ceza-kovusturma',
    category: 'CEZA HUKUKU',
    term: 'KOVUŞTURMA',
    definition:
      'Suç işlediği bildirilen kişi hakkında adlî takip yapılması süreci; iddianamenin kabulü ile hükmün kesinleşmesine kadar geçen evre.',
  },

  // BORÇLAR HUKUKU
  {
    id: 'borclar-haksiz-fiil',
    category: 'BORÇLAR HUKUKU',
    term: 'HAKSIZ FİİL',
    definition:
      'Bir kimsenin hukuka aykırı olarak başka bir kişiye zarar vermesi.',
  },
  {
    id: 'borclar-rehin',
    category: 'BORÇLAR HUKUKU',
    term: 'REHİN HAKKI',
    definition:
      'Bir alacağın yerine getirilmemesi durumunda, taşınır veya taşınmaz maldan öncelikli tahsil hakkı.',
  },
  {
    id: 'borclar-bagislama',
    category: 'BORÇLAR HUKUKU',
    term: 'BAĞIŞLAMA',
    definition:
      'Bir malın karşılıksız olarak başka birine devredilmesi işlemi.',
  },
  {
    id: 'borclar-zamanasimi',
    category: 'BORÇLAR HUKUKU',
    term: 'ZAMANAŞIMI',
    definition:
      'Belirli bir sürenin geçmesiyle hak kazanma veya yükümlülükten kurtulma durumu.',
  },
  {
    id: 'borclar-edim',
    category: 'BORÇLAR HUKUKU',
    term: 'EDİM',
    definition:
      'Borçlunun borcun konusunu yerine getirmesi gereken davranış; verme, yapma, yapmama şeklinde olabilir.',
  },

  // İDARE HUKUKU
  {
    id: 'idare-belediye',
    category: 'İDARE HUKUKU',
    term: 'BELEDİYE MECLİSİ',
    definition:
      'Seçimle gelen, bütçe yapma, vergi düzenleme gibi konularda karar veren belediye organı.',
  },
  {
    id: 'idare-danistay',
    category: 'İDARE HUKUKU',
    term: 'DANIŞTAY',
    definition: 'Yüksek idare mahkemesi; danışma ve inceleme mercii.',
  },
  {
    id: 'idare-vazife',
    category: 'İDARE HUKUKU',
    term: 'VAZİFE',
    definition:
      'Görev; mahkemelerin hangi tür davalara bakacağını belirleyen yetki kuralları.',
  },
  {
    id: 'idare-yerel',
    category: 'İDARE HUKUKU',
    term: 'YEREL MAHKEME',
    definition: 'Olayı ilk derecede gören mahkeme; mahallî mahkeme.',
  },
  {
    id: 'idare-vali',
    category: 'İDARE HUKUKU',
    term: 'VALİ',
    definition:
      'İlde, hükümetin temsilcisi olarak görev yapan ve idari işleri yürüten kişi.',
  },
];
