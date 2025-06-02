import Layout from '../components/Layout';

function CaseStudy() {
  return (
    <Layout>
      <div className="flex  overflow-hidden">
        {/* Sol taraf - Olay */}
        <div className="w-1/2 m-6 p-6 rounded-lg h-screen overflow-y-auto bg-white text-gray-800 border-r">
          <h2 className="text-lg font-semibold mb-4">OLAY</h2>
          <p className="mb-4">
            Kampüste öğle saatlerinde, iki öğrenci olan Savaş ve Barış arasında
            bir sözlü tartışma başlar. Barış, Savaş’ın önceden anlaşmalarına
            rağmen sınavda kendisine kopya vermemesi üzerine Savaş’a “
            <strong>kaypak, senden de ne beklenirdi ki zaten...</strong>”
            demiştir.
          </p>
          <p className="mb-4">
            Tartışma, Savaş’ın Barış’a fiziksel olarak saldırmasıyla kavgaya
            dönüşür. Kampüs güvenliği olaya müdahale eder ve polisi çağırır.
            Polis olay yerine gelir ve tarafların ifadelerini alır.
          </p>
          <p className="mb-4">
            Savaş, olayın anlık öfkeyle gerçekleştiğini ve pişman olduğunu
            belirtirken, Barış ise saldırının Savaş’ın kendisinde duyduğu öfke
            nedeniyle gerçekleştiğini iddia eder. Kampüs güvenliği ve birkaç
            öğrenci tanık olarak ifadelerini verir. Barış hastaneye kaldırılır
            ve tedavi altına alınır.
          </p>
          <p className="mb-4">
            Hastane, Barış’ın darp nedeniyle burnunun kırıldığını bildirir.
            Barış, kamu davası dışında ayrıca hukuki danışmanlık alır ve Savaş
            hakkında kasten yaralama suçlamasında bulunur. Barış’ın hastane
            raporu da delil olarak sunulur. Savaş’ın avukatı, Savaş’ın
            pişmanlığını ve olayın anlık öfkeyle gerçekleştiğini ileri sürerek
            cezada indirim talebinde eder. Mahkeme, Savaş’ın kasten yaralama
            suçunu işlediğine, ancak pişmanlık ve haksız tahrik nedenleriyle
            cezasında indirim uygular. Savaş’a belirli bir süre hapis cezası
            verilir ve bu cezanın ertelenmesine karar verilir. Barış’ın
            zararları da tazmin edilir.
          </p>
        </div>

        {/* Sağ taraf - Sorular */}
        <div className="w-1/2 m-6 p-6 rounded-lg overflow-y-auto bg-gray-50 text-gray-900 relative">
          {/* Sabit üst başlık */}
          <div className="sticky top-0 bg-gray-50 pb-4 z-10">
            <div className="text-sm text-right font-medium mb-2">
              Dr. Öğr. Üyesi Ümmügülsüm KILIÇ
            </div>
            <h2 className="text-lg font-semibold">Sorular:</h2>
          </div>

          <ol className="list-decimal list-inside space-y-6 mt-4">
            <li>
              Savaş’ın pişmanlık ve tahrik durumları ceza hukukunda nasıl
              değerlendirilmektedir? Bu durumların ceza indirimi üzerindeki
              etkilerini açıklayınız.
            </li>
            <textarea className="mt-8 h-28 w-full border-t border-gray-300 pt-4 text-gray-500 text-sm">
              Bu alana öğrencinin cevapları yazması beklenmektedir.
            </textarea>
            <li>
              Barış’ın tartışma sırasında Savaş’a yönelik hakaret veya küçük
              düşürücü ifadeler kullanıp kullanmadığını değerlendiriniz. İfade
              özgürlüğünün sınırları ve hakaret suçunun nasıl hukuki bir
              çerçevede ele alınacağını açıklayınız.
            </li>
            <textarea className="mt-8 h-28 w-full border-t border-gray-300 pt-4 text-gray-500 text-sm">
              Bu alana öğrencinin cevapları yazması beklenmektedir.
            </textarea>
            <li>
              Kasten yaralama suçunun hukuki tanımını yapınız. Savaş’ın
              eyleminin kasten yaralama suçu oluşturup oluşturmadığını ve bu
              suçun unsurlarını tartışınız. Savaş’ın eylemi bu unsurları taşıyor
              mudur? Açıklayınız. <br />
              <span className="italic">
                (Suçun unsurları, objektif ve subjektif unsurlar, fiil, netice,
                illiyet bağı)
              </span>
            </li>
            <textarea className="mt-8 h-28 w-full border-t border-gray-300 pt-4 text-gray-500 text-sm">
              Bu alana öğrencinin cevapları yazması beklenmektedir.
            </textarea>
          </ol>
        </div>
      </div>
    </Layout>
  );
}

export default CaseStudy;
