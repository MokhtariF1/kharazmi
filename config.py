bot_token = "8062992246:AAEqcMXPAFxw681n00HrLyGFXT4mKVEgYO4"
api_id = 28482138
api_hash = "cdcd9c0f111f85feaafac50d1bc3d6a5"
proxy = False
proxy_address = ("socks5", "127.0.0.1", 27017)


bot_text = {
    "start": "سلام دانشجوی عزیز، به ربات تست مینی دوره فنگشویی خوش آمدید",
    "start_test": "شروع آزمون💫",
    "information": "🧑اطلاعات کاربری",
    "no_score_start": "سلام دوست عزیز تست فنگشویی سطح انرژی محیط شما برای آموزش مینی دوره فنگشویی پاسخگویی تست ضروریست\nبرای شروع تست روی دکمه زیر کلیک کنید",
    "start_test_text": "دانشجوی گرامی لطفا سوالات تست زیر راجواب دهید این تست شامل ۱۴ سوال است لطفا سعی کنید زیرده دقیقه جواب دهید.",
    "a": "الف",
    "b": "ب",
    "c": "پ",
    "d": "ت",
    "e": "ث",
    "f": "ج",
    "g": "ع",
    "h": "د",
    "i": "ی",
    "question_1": "من ....\nالف)شغلم را دوست دارم و درآمد خوبی دارم\nب)شغلم را دوست دارم ولی درآمد کمی دارم\nپ)شغلم و درآمدم را دوست ندارم و میخواهم آن را عوض کنم",
    "cancel": "انصراف از آزمون",
    "canceled": "با موفقیت کنسل شد",
    "question_2": "من تقریبا....\nالفه)هرماه سفر میرم\nب)سالی ۲ الی ۳ بار سفر میرم\nپ)چند ساله سفر نرفته ام",
    "question_3": "وضعیت روابط عاشقانه\nالف)متاهلم(یادر رابطه هستم)رابطه عالی دارم\nب)متاهلم(یا در رابطه هستم)رابطه خوبی ندارم\nپ)مجردم و کسی توی زندگیم نیست",
    "question_4": "وضعیت سلامتی و بیماری\nالف)خداروشکر که از سلامتی کافی برخوردارم\nب)هر ماه اعضای خانواده من مریض میشوند\nپ)متاستفانه در بیماری طولانی مدت هستم",
    "question_5": "وضعیت روابط با نزدیکان\nالف)با دوستان و فامیل رابطه عالی دارم\nب)متاستفانه با نزدیکانم روابط خوبی ندارم\nپ)تنهایم و با کسی رابطه خوبی ندارم",
    "question_6": "وضعیت فرزندان\nالف)فرزندان خوب و مطیعی دارم\nب)فرزندان پرخاشگر و بی توجه به تحصیل دارم\nپ)میخواهم مادر شوم\nت)فرزند ندارم",
    "question_7": "درآمد من...\nالف)زیر ۱۰ میلیون است\nب)بین ۱۰ تا ۲۰ میلیون است\nپ)۲۵ میلیون به بالاست",
    "question_8": "زمانی که تصمیم به انجام کاری میگیرید آن کار چطور پیش میرود؟\nالف)آسان و راحت به نتیجه مورد نظر میرسم\nب)خیلی سخت نتیجه میگیرم یا رهایش میکنم و آن کار را به سر انجام نمیرسونم",
    "next_questions": "دانشجوی عزیز در سوالات بعدی در صورتیکه جهت قرارگیری هر قسمت از خانه خود را میدانید آن را انتخاب کنید در غیر اینصورت بر روی گزینه نمیدانم کلیک کنید",
    "question_9": "درب ورودی شما در کدام جهت از نقشه خانه شما قرار گرفته است؟\nالف)شمال\nب)شرق\nپ)جنوب\nت)غرب\nث)شمال شرقی\nج)جنوب شرقی\nع)جنوب غربی\nد)شمال غربی\nی)نمیدانم",
    "question_10": "آشپزخانه شما در کدام جهت از نقشه خانه شما قرار گرفته است؟\nالف)شمال\nب)شرق\nپ)جنوب\nت)غرب\nث)شمال شرقی\nج)جنوب شرقی\nع)جنوب غربی\nد)شمال غربی\nی)نمیدانم",
    "question_11": "سرویس بهداشتی و حمام شما در کدام جهت از نقشه خانه شما قرار گرفته است؟\nالف)شمال\nب)شرق\nپ)جنوب\nت)غرب\nث)شمال شرقی\nج)جنوب شرقی\nع)جنوب غربی\nد)شمال غربی\nی)نمیدانم",
    "question_12": "اتاق زوجین در کدام جهت از نقشه خانه شما قرار گرفته است؟\nالف)شمال\nب)شرق\nپ)جنوب\nت)غرب\nث)شمال شرقی\nج)جنوب شرقی\nع)جنوب غربی\nد)شمال غربی\nی)نمیدانم",
    "question_13": "اتاق فرزندان در کدام جهت از نقشه خانه شما قرار گرفته است؟\nالف)شمال\nب)شرق\nپ)جنوب\nت)غرب\nث)شمال شرقی\nج)جنوب شرقی\nع)جنوب غربی\nد)شمال غربی\nی)نمیدانم",
    "question_14": "آیا در منزل شما یک یا همه موارد زیر موجود است؟",
    "yes": "بله",
    "no": "خیر",
    "result": "نتیجه تست شما:باتوجه به کسب {score} از ۱۰۰ امتیاز سطح انرژی محیط شما:\n{test_result}\n\nمن مریم پیروی فر مدرس فنگشویی خوشحالم که افراد دغدغه مندی مثل شمارا راهنمایی میکنم امیدوارم با انجام دادن تست و آموزش رایگان مینی دوره سطح انرژی های اطرافتون را به حداقل برسونید و بهترین نتیجه را از آموزشها داشته باشید",
}