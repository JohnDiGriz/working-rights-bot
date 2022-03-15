import logging
from telegram import ReplyKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = os.environ["TOKEN"]
CHAT = os.environ["CHAT"]

basic_responses = { "Працедавець відмовляється платити заробітну плату, мотивуючи це війною":
                      """Війна це офіційно підтверджений форс\-мажор \(заява \-промислової палати, далі \- ТПП\)  https://ucci\.org\.ua/press\-center/ucci\-news/protsedura\-zasvidchennia\-fors\-mazhornikh\-obstavin\-z\-28\-02\-2022\. Форс\-мажор тобто обставина непереборної сили може бути причиною не виконання певних зобов'язань, прописаних у трудовому договорі\. Однак для цього працедавець повинен звернутися до регіонального відділення ТПП та отримати сертифікат, що **підтверджує форс\-мажор для конкретного договору та неможливість виконання своїх зобов'язань у даний момент**\. Без цього сертифіката працедавець не може відмовитися від виконання своїх зобов'язань, зокрема від зобов'язання вчасно виплачувати заробітну плату\. 
Джерело: https://biz\.ligazakon\.net/analitycs/209892_vikonannya\-dogovrnikh\-zobovyazan\-ta\-fors\-mazhor

Що робити? 
Рекомендуємо діяти в такому порядку:
1\. Написати письмову вимогу про погашення заборгованості до керівника підприємства\. 
2\. З цією інформацією звернутися на Урядову **гарячу лінію: 1545**\. 
3\. Надати колективне письмове звернення до органів влади\. Рекомендуємо написати омбудсмену, Держпраці та поліції, але також місцевим органам влади та органам місцевого самоврядування

❗️ Повідомляємо, що безпідставна невиплата заробітної більше як за місяць ━ **це злочин**, який карається згідно статті 175 Кримінального кодексу України \(далі ━ ККУ\)\. В такому випадку слід звертатися до поліції\. 

❗️ Якщо відбувається неповна виплата зарплати, то працедавця можна притягнути **до адмінвідповідальності** згідно статті 41 Кодексу України про адміністративні правопорушення \(далі ━ КУпАП\)\. Цим займається Держпраці\. 

❗️ Також "Соціальний рух" **може висвітлити ваш кейс в інформаційному просторі**, якщо ви назвете підприємство і кількість працівників, перед якими є борг\. Постарайтеся також зібрати документальні свідоцтва відмови вашого працедавця виплачувати зарплату \- скріншоти листування в месенджерах, фото письмової вимоги до керівника тощо\.
""",
                      "Працедавець примусово відправляє у неоплачувану відпустку або намагається звільнити": 
                      """Війна не дозволяє працедавцю відправити вас у неоплачувану відпустку без вашої згоди та письмової заяви від вас \(ст\. 84 КЗпП України та стаття 25 закону України "Про відпустку"\)\.

Якщо робота підприємства стала неможливою та працедавець хоче скоротити вас чи ліквідувати підприємство, він повинен виплатити вам вихідну допомогу\. Відповідно п\. 1 ст\. 40 КЗпП у разі ліквідації підприємства або припинення ФОП, скорочуючи штат, працедавці повинні **попередити працівників за 2 місяці та виплатити вихідну допомогу** у розмірі одного місячного заробітку (ст\. 44 КЗпП)\. Кошти на це вони повинні знайти самі\. 

Якщо працедавець не хоче ліквідувати підприємство або скорочувати співробітників, він повинен оголосити простій згідно зі статтею 34, 113 КЗпП України\. Цей режим роботи передбачає **виплату зарплати у ⅔ від тарифної сітки**\.""",
                      "Працедавець відмовляється виплачувати понаднормові/нічні/будь\-які інші види доплат": 
                       """На період воєнного стану **не скасовуються** ані доплати за надурочні, ані за роботу вночі\.

Якщо вас цікавить, чи входять ці доплати до складу зарплати медиків, ━ ознайомтеся з матеріалом\. В ньому сказано, що ці доплати "поглинаються" \(проте зарплата все одно має становити до оподаткування 13700 грн\)\.

Джерело: https://www\.golovbukh\.ua/article/7578\-oplata\-prats\-derjavn\-garant""",
                      "Я залишися_ась без роботи через війну. Яку допомогу від держави я можу отримати?": 
                       """Після затвердження постанови КМУ від 04\.03\.22 №199 деяких застрахованих осіб, які втратили можливість працювати, є право звернутися за допомогою за програмою єПідтримка \(6500 грн\)\. Це працівники і гіг\-працівники \(за винятком тих, хто працює в бюджетних установах і фондах соцстрахування\)\. Також таку допомогу можуть отримати певні категорії ФОП\. 
**Важливо!** Допомога виплачується особам, які проживають на територіях, де ведуться бойові дії\. Список таких територій визначає ДСНС \(https://dsns\.gov\.ua/\)\. На даний момент це такі області: Чернігівська, Сумська, Харківська, Херсонська, Миколаївська, Запорізька, Донецька, Луганська, Житомирська, Одеська, Волинська, Київська та місто Київ\.  
Слід зазначити, що є регіони, де існує ризик авіаударів, проте бойові дії там не ведуться, ━ такі особи не можуть претендувати на виплату за програмою єПідтримка\.

У законодавстві існують певні компенсаційні механізми, що покликані зменшити тягар для працедавців\. Існує допомога по частковому безробіттю, яка виплачується за рахунок Фонду соціального страхування України на випадок безробіття у тих випадках, коли економічна діяльність вимушено припиняється\. 
Допомога, передбачена постановою КМУ №74, виплачується працівникам виробничих підприємств, а допомога, передбачена постановою КМУ №306, ━ у зв'язку з карантином\. Слід розуміти, що розмір компенсації доволі обмежений і бюджетних коштів на виплату допомогу по частковому безробіттю не передбачено\.""",
                      "Я мобілізувався_ась / пішов_ла добровольцем у Територіальну Оборону (ТрО)": 
                       """Відповідно до статті 119 КЗпП на час виконання державних або громадських обов’язків, якщо за чинним законодавством України ці обов’язки можуть здійснюватися у робочий час, працівникам гарантується збереження місця роботи і середнього заробітку\.

Ті самі гарантії надаються добровольцям ТрО\. Згідно з частиною другою статті 24 Закону України „Про основи національного спротиву” на членів добровольчих формувань територіальних громад під час їх участі у заходах підготовки добровольчих формувань територіальних громад, а також виконання ними завдань територіальної оборони поширюються гарантії соціального і правового захисту, передбачені Законом України „Про соціальний і правовий захист військовослужбовців та членів їх сімей”""",
                      "Я евакуювався_лась / втратив_ла зв'язок із працедавцем / не можу потрапити на робоче місце через бойові дії": """""",
                      "Якої позиції дотримуватися на переговорах з працедавцем?": 
                       """Якщо ви не можете потрапити на робоче місце, але при цьому роботу можна продовжити в дистанційному режимі \- через інтернет та інші засоби зв'язку \- може перевести співробітника на віддалену роботу не змінюючи трудового договору, для цього достатньо розпорядження керівника \(стаття 60\-2 КЗпП\)\.

Якщо ж працівник не може вийти на роботу через бойові дії, то він **не може бути звільнений або відправлений у відпустку заднім числом**\. Роботодавець повинен вважати це відсутністю на робочому місці з поважних причин і не має права ставити в табелі обліку використання робочого місця позначки про прогул, а також зобов'язаний виплачувати заробітну плату у повному обсязі\.

У випадках коли зв'язок із працівником втрачено і не зрозуміло, що з ним сталося, роботодавець повинен використовувати позначку «I» – інші причини неявок або «НЗ» – неявка з нез'ясованих причин\. Після з'ясування обставин та виявлення, що причини були поважними, табель обліку використання робочого часу необхідно скоригувати\.

Джерело: https://www\.me\.gov\.ua/Documents/Detail?lang=uk\-UA&id=10d196f4\-2218\-45bd\-a6df\-34048ce35032&title=VidpovidiNaPoshireniPitanniaZiSferiTrudovikhVidnosinVUmovakhVonnogoChasu&fbclid=IwAR0rHIq_248U1WzKDUBP54DvAlIZFwJ1samUecikXymHb9lecHLHgBgNELg"""}



def start(update, context):
    keyboard = [["Працедавець відмовляється платити заробітну плату, мотивуючи це війною"],
                ["Працедавець примусово відправляє у неоплачувану відпустку або намагається звільнити"],
                ["Працедавець відмовляється виплачувати понаднормові/нічні/будь-які інші види доплат"],
                ["Я залишися_ась без роботи через війну. Яку допомогу від держави я можу отримати?"],
                ["Я мобілізувався_ась / пішов_ла добровольцем у Територіальну Оборону (ТрО)"],
                ["Я евакуювався_лась / втратив_ла зв'язок із працедавцем / не можу потрапити на робоче місце через бойові дії"],
                ["Якої позиції дотримуватися на переговорах з працедавцем?"]]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text("""Привіт!

Цей бот створили активісти ГО "Соціальний рух", щоб консультувати вас на рахунок порушення трудових прав.

Будь ласка, напишіть своє звернення, або виберіть одну з опцій
Ми відповімо вам у найближчий час.""", reply_markup = reply_markup)
    



def receive_complaint(update, context):
    if update.message.text in basic_responses:
      update.message.reply_text(basic_responses[update.message.text], parse_mode=ParseMode.MARKDOWN_V2)
    else:
      update.message.reply_text("""Ваше звернення прийняте""")
      update.message.forward(chat_id=CHAT)
      context.bot.send_message(chat_id=CHAT, text="@"+update.message.from_user.username)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(MessageHandler(Filters.text, receive_complaint))

    dp.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url='https://working-rights-bot.herokuapp.com/' + TOKEN)

    updater.idle()


if __name__ == '__main__':
    main()
