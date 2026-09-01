# Waslni (وصلني) — Matching / Dating Website

A real, working dating & matching website built with **Django** (Python).
Inspired by BuzzArab: users register, build a profile, browse (swipe) other
profiles, like/pass, get matched on mutual likes, and chat with their matches.

## Features
- Custom registration with 18+ age validation (`accounts` app)
- Login / logout / auth-protected pages (Django's built-in auth system)
- Profile: photo, birth date → age, gender, looking for, city, country, bio
- Discover / swipe screen with Like ❤️ and Pass ✕
- Automatic mutual-match detection (`matching` app)
- Matches list + 1-to-1 chat per match (`chat` app)
- Django Admin panel to manage users, profiles, likes, matches, messages

## Project structure
```
matchsite/
├── accounts/     # custom registration, login, profile
├── matching/     # Like / Pass / Match models + discover view
├── chat/         # messages between matched users
├── templates/    # HTML (Bootstrap 5)
├── static/css/   # styling
└── matchsite/    # Django project settings
```

## Setup (local)

```bash
# 1. Create a virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply database migrations
python manage.py migrate

# 4. Create an admin account
python manage.py createsuperuser

# 5. Run the dev server
python manage.py runserver
```

Then open http://127.0.0.1:8000/ — register a couple of test accounts
(in two different browsers, or one in incognito) to try the like → match →
chat flow yourself.

Admin panel: http://127.0.0.1:8000/admin/

## شرح بالدارجة

هذا مشروع Django حقيقي وخدام، فيه:
- **تسجيل ودخول** (accounts) — مع تحقق العمر لازم يكون +18
- **بروفايل** — صورة، تاريخ الميلاد (يحسب العمر وحدو)، جنس، شكون تحب تلقى، ولاية، بلد، نبذة
- **Discover** — تصفح البروفايلات وحدة وحدة، تعمل Like ولا Pass
- **Match** — إلا حبكم بعضاكم (Like متبادل)، تولي "match" وحدة توماتيكيا
- **Chat** — كل match عندو محادثة خاصة بيه

### كيفاش تخدمو عندك:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # باش تدخل لـ /admin/
python manage.py runserver
```
دير `http://127.0.0.1:8000/` فالمتصفح.

### رفع عدة صور فالبروفايل
دبا فـ "Edit profile" كاين حقل "Add more photos" تقدر تختار فيه بزاف صور فمرة وحدة (مع الصورة الرئيسية `photo`). كل صورة تتزاد فـ gallery تحت البروفايل، وتقدر تمسحها وحدة وحدة.

### الاستضافة (Hosting) — مجانا بالكامل، رابط عمومي يخدم من أي متصفح

غادي نستعملو **Render** (مجاني، بلا Credit Card، ويدعم دومين مخصص فالمستقبل بلاش).

**الخطوة 1 — رفعو المشروع لـ GitHub** (Render كيقرا الكود من GitHub):
```bash
git init
git add .
git commit -m "Waslni - matching website"
git branch -M main
git remote add origin https://github.com/USERNAME/waslni.git
git push -u origin main
```
(إلا ماعندكش repo، دير واحد جديد فـ https://github.com/new قبل هاد الخطوة، وخليه Public أو Private — الاثنين يخدمو مع Render)

**الخطوة 2 — دير حساب Render:**
- https://render.com → Sign up (تقدر تدخل بحساب GitHub تاعك مباشرة)

**الخطوة 3 — دير Web Service جديد:**
- من الداشبورد: **New +** → **Web Service**
- اختار الـ repo `waslni` من GitHub
- Render غايكتشف أوتوماتيكيا أنه Python — عمر هاد الحقول:
  - **Build Command:** `pip install -r requirements.txt`
  - **Start Command:** `python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn matchsite.wsgi:application`
  - **Instance Type:** Free

**الخطوة 4 — زيد Environment Variables** (فـ tab "Environment"):
| Key | Value |
|---|---|
| `SECRET_KEY` | أي نص طويل وعشوائي (بحال `k8x@92mQp!zR7...`) |
| `DEBUG` | `False` |

**الخطوة 5 — دوس "Create Web Service"**
Render غايبني وينشر الموقع (يدوم 2-5 دقايق فالمرة الأولى). من بعد غيعطيك رابط بحال:
```
https://waslni.onrender.com
```
هذا الرابط **عمومي، يخدم من أي متصفح وأي جهاز (بيسي، تيليفون...) وأي حد** تبعثله يقدر يدخل مباشرة بلا ما يحتاج ينصب حتى حاجة.

**الخطوة 6 — دير superuser على السيرفر الحقيقي** (باش تدخل لـ `/admin/`):
- فـ Render dashboard، دخل لـ tab **Shell** ديال الـ Web Service تاعك، وكتب:
```bash
python manage.py createsuperuser
```

**⚠️ حاجة خاصك تعرفها (Free tier limitation):**
- السيرفر المجاني "يرقد" إلا حتى حد ما زارو فـ 15 دقيقة (أول زيارة من بعد الرقاد تاخد ~30 ثانية باش السيرفر يفيق، طبيعي)
- التخزين مؤقت (ephemeral) — يعني الصور وقاعدة البيانات يمكن تتمسح كل ما تعاود تنشر (redeploy) نسخة جديدة من الكود. باش صحابك يجربو الموقع مزيان هاذي ماشي مشكل، بصح للاستعمال الحقيقي على المدى الطويل، فالمستقبل تقدر تربط قاعدة بيانات Postgres وتخزين صور دائم (بحال Cloudinary) — نقدر نديرها معاك وقتما بغيتي.

**دومين خاص بيك (`.com`) فالمستقبل:**
إلا بغيتي `waslni.com` عوض `waslni.onrender.com`: تشري الدومين من موقع بحال Namecheap (~10$/سنة)، ومن بعد فـ Render dashboard → tab **Custom Domains** → زيد الدومين → دير التعديلات اللي يطلبها فـ DNS settings تاع الدومين. الربط فحد ذاته مجاني.

### تسجيل الدخول بـ Google (Sign in with Google)

دبا الموقع فيه طريقتين للتسجيل/الدخول: **يوزرنيم + كلمة السر** (كيما كان)، أو **Google** (جديد). زوج الطرق كيحفظو الحساب فقاعدة البيانات، وأي حد يقدر يختار اللي يريحو.

باش تخدم أزرار "Continue with Google" خاصك تجيب مفاتيح مجانية من Google (Google ما تخليكش تستعمل زر Google بلا ما تسجل عندها التطبيق تاعك — الخدمة نفسها **مجانية بالكامل**، غير إجراء إداري):

1. روح لـ **https://console.cloud.google.com/** ودخل بحساب Gmail تاعك
2. أنشئ مشروع جديد (New Project) — سميه بحال `Waslni`
3. من القائمة على اليسار: **APIs & Services → OAuth consent screen** → اختار **External** → عمر الاسم/الإيميل → Save
4. بعدها **APIs & Services → Credentials → Create Credentials → OAuth client ID**
   - Application type: **Web application**
   - **Authorized redirect URIs**، زيد:
     ```
     https://waslni.onrender.com/accounts/google/login/callback/
     http://127.0.0.1:8000/accounts/google/login/callback/
     ```
     (بدل `waslni.onrender.com` برابط الموقع الحقيقي تاعك كي تنشرو، وإلا بدلتيه فالمستقبل زيد الرابط الجديد هنا زيادة)
5. Google غايعطيك **Client ID** و **Client Secret** — نسخهم
6. زيدهم كـ Environment Variables (فـ Render/PythonAnywhere، ولا فـ `.env` محليا):
   | Key | Value |
   |---|---|
   | `GOOGLE_CLIENT_ID` | القيمة اللي عطاتك Google |
   | `GOOGLE_CLIENT_SECRET` | القيمة اللي عطاتك Google |

7. `python manage.py migrate` (باش يزيد جداول allauth الجديدة) — من بعد `python manage.py runserver` أو تنشرو من جديد

**ملاحظة مهمة:** مستخدم دخل بـ Google ما عندوش تاريخ ميلاد ولا جنس محددين مباشرة من Google، فالموقع غايوجهو أوتوماتيكيا لصفحة "Edit profile" باش يكمل هاد المعلومات (وتحقق +18 خدام هنا زيد) قبل ما يقدر يشوف بروفايلات آخرين.

### نسيان كلمة السر (Forgot password)

دبا كاين رابط "Forgot your password?" فصفحة الدخول: المستخدم كيدخل الإيميل تاعو، كيوصلو إيميل فيه رابط (يخدم مرة وحدة وينتهي بعد يوم)، كيدوس عليه، كيدير كلمة سر جديدة، ويرجع يدخل.

باش الإيميل يوصل بصح (ماشي غير يبان فـ terminal)، خاصك تعطي للموقع حساب Gmail يبعث بيه — **مجاني بالكامل**:

1. دير حساب Gmail (إلا معندكش واحد جاهز)
2. فعل **2-Step Verification** فحسابك (myaccount.google.com/security)
3. من بعد روح لـ **myaccount.google.com/apppasswords**، دير App password جديد (اختار اسم بحال "Waslni"), Google غايعطيك كود من 16 حرف
4. زيد هاذوك الـ Environment Variables فـ Render/PythonAnywhere:
   | Key | Value |
   |---|---|
   | `EMAIL_HOST_USER` | الإيميل تاع Gmail تاعك (بحال `waslni.app@gmail.com`) |
   | `EMAIL_HOST_PASSWORD` | الكود ديال 16 حرف اللي عطاتك Google (App Password، ماشي كلمة السر العادية) |

من غير هاذوك المتغيرين (محليا فالبيسي تاعك مثلا)، الإيميلات غايبانو غير فـ terminal بحال قبل — مفيد للتجربة بلا ما تحتاج حساب حقيقي.

### أفكار للتطوير مستقبلا
- WebSocket/real-time chat (بحال Django Channels)
- بحث فلترة أكثر (بالعمر، المسافة...)
- تفعيل الحساب بالإيميل
- قاعدة بيانات وتخزين صور دائمين (Postgres + Cloudinary) على Render
