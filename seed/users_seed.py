# cSpell:disable

from models import db, User


seed = [
    ("Password1234$", "Charlena", "Meanwell", "cmeanwell0@t-online.de", True, 53.3734053, -6.3695384),
    ("Password1234$", "Mandi", "Pitbladdo", "mpitbladdo1@odnoklassniki.ru", True, 29.176523, 120.390932),
    ("Password1234$", "Corrina", "Trahearn", "ctrahearn2@baidu.com", True, 26.610707, 115.81778),
    ("Password1234$", "Galvin", "Bogace", "gbogace3@cbc.ca", True, 17.9567646, -102.1943485),
    ("Password1234$", "Bryna", "Sainte Paul", "bsaintepaul4@archive.org", True, 49.0549661, 16.6445006),
    ("Password1234$", "Alanson", "Monnoyer", "amonnoyer5@dailymotion.com", True, 45.8206187, -73.9300943),
    ("Password1234$", "Etti", "Restill", "erestill6@phoca.cz", True, -7.5882979, 109.1553021),
    ("Password1234$", "Xena", "Greguoli", "xgreguoli7@meetup.com", True, 48.9066299, 2.2456603),
    ("Password1234$", "Rebecca", "Romain", "rromain8@hostgator.com", True, 28.39895, 113.02064),
    ("Password1234$", "Tiffany", "Eliassen", "teliassen9@mediafire.com", True, 41.1872522, -8.434873),
    ("Password1234$", "Florrie", "McAlroy", "fmcalroya@netvibes.com", True, 59.3030191, 14.0706348),
    ("Password1234$", "Simone", "Paolazzi", "spaolazzib@google.ca", True, -6.8272662, 111.2874835),
    ("Password1234$", "Nap", "McGarvey", "nmcgarveyc@google.com.br", True, -5.4430889, -35.8716137),
    ("Password1234$", "Odessa", "Lavalde", "olavalded@jugem.jp", True, 26.0824759, 119.2969454),
    ("Password1234$", "Langston", "Godwyn", "lgodwyne@rediff.com", True, 52.35536, 16.519559),
    ("Password1234$", "Titos", "Yurocjkin", "tyurocjkinf@yahoo.co.jp", True, 32.703801, 35.225489),
    ("Password1234$", "Camellia", "Ragg", "craggg@mozilla.com", True, 13.0748879, 120.7213113),
    ("Password1234$", "Cacilia", "Clace", "cclaceh@g.co", True, -18.2074524, -65.1847957),
    ("Password1234$", "Joseph", "Byrcher", "jbyrcheri@quantcast.com", True, -7.2760371, 107.6925674),
    ("Password1234$", "Sibelle", "Burghill", "sburghillj@tumblr.com", True, -7.9431343, 112.6183751),
    ("Password1234$", "Fredericka", "Soaper", "fsoaperk@ebay.co.uk", True, 29.654838, 91.140552),
    ("Password1234$", "Amandy", "Cuardall", "acuardalll@ft.com", True, 25.6279123, 88.6331758),
    ("Password1234$", "Roddie", "Erridge", "rerridgem@google.com.au", True, 15.7290855, 120.6271711),
    ("Password1234$", "Torie", "Craggs", "tcraggsn@pagesperso-orange.fr", True, 39.73287, 98.494548),
    ("Password1234$", "Faustine", "Northway", "fnorthwayo@mediafire.com", True, 53.068264, 16.136353),
    ("Password1234$", "Akim", "Zukerman", "azukermanp@w3.org", True, 13.26831, 43.50993),
    ("Password1234$", "Tawnya", "Warriner", "twarrinerq@cyberchimps.com", True, 37.8163881, 66.0285106),
    ("Password1234$", "Mart", "Grant", "mgrantr@ed.gov", True, 29.233463, 119.902455),
    ("Password1234$", "Alexandre", "Coonan", "acoonans@odnoklassniki.ru", True, 31.825073, 119.944048),
    ("Password1234$", "Sydney", "Youngman", "syoungmant@pen.io", True, 3.7144776, 96.8324201),
    ("Password1234$", "Tandie", "Garling", "tgarlingu@about.com", True, 61.7983586, 34.3753781),
    ("Password1234$", "Anjanette", "Nehl", "anehlv@hostgator.com", True, 12.5951892, 6.5863469),
    ("Password1234$", "Ashil", "Haile", "ahailew@loc.gov", True, 31.1447, 61.7925),
    ("Password1234$", "Mahalia", "De Laspee", "mdelaspeex@artisteer.com", True, -21.7972251, -50.879763),
    ("Password1234$", "Inigo", "Dur", "idury@va.gov", True, -27.4369394, -51.2213044),
    ("Password1234$", "Richie", "Gounel", "rgounelz@jimdo.com", True, -6.3079232, 107.172085),
    ("Password1234$", "Madelyn", "Banasevich", "mbanasevich10@salon.com", True, -8.1095216, 111.8330962),
    ("Password1234$", "Tate", "Bollans", "tbollans11@columbia.edu", True, -8.3162857, 124.3654402),
    ("Password1234$", "Henryetta", "Hurles", "hhurles12@loc.gov", True, -7.0631844, 107.7843483),
    ("Password1234$", "Caitrin", "Canet", "ccanet13@ucsd.edu", True, -6.8268504, 111.8359916),
    ("Password1234$", "Aggie", "Kohrsen", "akohrsen14@webmd.com", True, 39.8314629, 116.3220944),
    ("Password1234$", "Carita", "Hessentaler", "chessentaler15@loc.gov", True, 41.2022247, -8.5597719),
    ("Password1234$", "Marcia", "Stinton", "mstinton16@google.com.hk", True, 48.659828, 102.625198),
    ("Password1234$", "Tabby", "Conway", "tconway17@si.edu", True, -11.6557739, 43.26505),
    ("Password1234$", "Helge", "Cowton", "hcowton18@vinaora.com", True, 31.04808, 121.749495),
    ("Password1234$", "Hank", "Costin", "hcostin19@indiatimes.com", True, 49.2706048, -1.6509128),
    ("Password1234$", "Kary", "Udie", "kudie1a@posterous.com", True, -22.7338724, -45.1201112),
    ("Password1234$", "Elden", "Baline", "ebaline1b@japanpost.jp", True, 52.87728, 15.52966),
    ("Password1234$", "Levey", "Joannet", "ljoannet1c@ucoz.ru", True, 46.8311732, 35.7512432),
    ("Password1234$", "Corby", "Croote", "ccroote1d@reference.com", True, 57.670116, 66.1742259),
    ("Password1234$", "Angeline", "Trickett", "atrickett1e@smugmug.com", True, 55.7784607, 27.9323817),
    ("Password1234$", "Inessa", "Paddefield", "ipaddefield1f@people.com.cn", True, 12.0683397, 99.8459774),
    ("Password1234$", "Ellissa", "Streater", "estreater1g@mayoclinic.com", True, 1.6940945, -76.2363248),
    ("Password1234$", "Judye", "McIlwain", "jmcilwain1h@stumbleupon.com", True, -18.2898667, 32.043969),
    ("Password1234$", "Jaclin", "MacCracken", "jmaccracken1i@nyu.edu", True, -26.9655922, -50.4178973),
    ("Password1234$", "Alisha", "D'Antuoni", "adantuoni1j@pagesperso-orange.fr", True, -21.4261129, -45.9481612),
    ("Password1234$", "Morgen", "Flight", "mflight1k@360.cn", True, 51.4556245, 15.0831462),
    ("Password1234$", "Alwin", "Dibsdale", "adibsdale1l@businessweek.com", True, -6.6038889, 107.0527778),
    ("Password1234$", "Lemar", "Kilfoyle", "lkilfoyle1m@telegraph.co.uk", True, 23.0365513, -81.2133262),
    ("Password1234$", "Lavinie", "Dumper", "ldumper1n@geocities.jp", True, 61.7968844, 25.7035513),
    ("Password1234$", "Isacco", "Carnegie", "icarnegie1o@nationalgeographic.com", True, 38.8777496, 141.6136391),
    ("Password1234$", "Shirley", "Rubenfeld", "srubenfeld1p@hexun.com", True, 30.7016468, 104.0663422),
    ("Password1234$", "Amelita", "Meconi", "ameconi1q@instagram.com", True, -28.9481925, -51.0749483),
    ("Password1234$", "Ben", "Van der Brug", "bvanderbrug1r@virginia.edu", True, 9.7907348, -13.5147735),
    ("Password1234$", "Pauletta", "Noyce", "pnoyce1s@wufoo.com", True, 37.9697625, 140.7803658),
    ("Password1234$", "Eve", "Mordan", "emordan1t@mozilla.com", True, 14.4712676, 121.0441201),
    ("Password1234$", "Vidovik", "Marland", "vmarland1u@twitpic.com", True, -40.2458577, 175.5482901),
    ("Password1234$", "Vittoria", "Jakubovsky", "vjakubovsky1v@1und1.de", True, -7.1234674, 111.8479156),
    ("Password1234$", "Ulrich", "Dummigan", "udummigan1w@nasa.gov", True, 45.5641261, 5.9680907),
    ("Password1234$", "Herbert", "Badder", "hbadder1x@google.com.au", True, 72.79, -56.130556),
    ("Password1234$", "Craggie", "Yarrell", "cyarrell1y@cornell.edu", True, 46.426574, 14.0833019),
    ("Password1234$", "Yank", "Filochov", "yfilochov1z@skyrock.com", True, 38.7508367, -9.2843236),
    ("Password1234$", "Jamaal", "Roskeilly", "jroskeilly20@digg.com", True, 14.582807, 121.061708),
    ("Password1234$", "Moshe", "Dullaghan", "mdullaghan21@photobucket.com", True, -8.4378527, 115.180023),
    ("Password1234$", "Dari", "Peddowe", "dpeddowe22@smugmug.com", True, -8.0138, 111.4166),
    ("Password1234$", "Dukie", "Tambling", "dtambling23@wix.com", True, 40.4742778, 49.8255553),
    ("Password1234$", "Caty", "Deam", "cdeam24@blogtalkradio.com", True, 49.830017, 21.14379),
    ("Password1234$", "Iolande", "Dallon", "idallon25@moonfruit.com", True, 39.918983, 116.47861),
    ("Password1234$", "Lazare", "Dossettor", "ldossettor26@scientificamerican.com", True, 36.57863, 114.114634),
    ("Password1234$", "Luelle", "Teal", "lteal27@jiathis.com", True, 7.2484596, 125.0587505),
    ("Password1234$", "Jackson", "Gleadhell", "jgleadhell28@europa.eu", True, 29.454189, 119.996847),
    ("Password1234$", "Erek", "Cardenosa", "ecardenosa29@washington.edu", True, 43.2721945, 47.5220901),
    ("Password1234$", "Shurlocke", "McGann", "smcgann2a@columbia.edu", True, 39.7968818, -74.9245946),
    ("Password1234$", "Ashli", "Freke", "afreke2b@e-recht24.de", True, -6.3668625, 106.237505),
    ("Password1234$", "Kessia", "Civitillo", "kcivitillo2c@printfriendly.com", True, 51.5144022, 21.1235461),
    ("Password1234$", "Eddie", "Klassman", "eklassman2d@last.fm", True, -5.2932525, -48.5187229),
    ("Password1234$", "Dodi", "Havoc", "dhavoc2e@tripod.com", True, 52.1930413, 25.1471719),
    ("Password1234$", "Hope", "Leon", "hleon2f@hao123.com", True, 17.622182, 120.6190252),
    ("Password1234$", "Sissie", "Priddle", "spriddle2g@fc2.com", True, 31.092719, 93.812858),
    ("Password1234$", "Gale", "Brambell", "gbrambell2h@noaa.gov", True, 18.6220301, -99.1559935),
    ("Password1234$", "Elwyn", "Antoni", "eantoni2i@pagesperso-orange.fr", True, 45.0052663, 41.1199008),
    ("Password1234$", "Justino", "Traut", "jtraut2j@cbc.ca", True, 8.5328493, 124.5621837),
    ("Password1234$", "Elsey", "Attewill", "eattewill2k@weather.com", True, 22.765392, 112.964446),
    ("Password1234$", "Shannen", "Veltmann", "sveltmann2l@icio.us", True, 14.6640555, 120.9712983),
    ("Password1234$", "Garrik", "Elloway", "gelloway2m@boston.com", True, 46.1298241, 14.5577637),
    ("Password1234$", "Gui", "Martschke", "gmartschke2n@netvibes.com", True, -21.2846176, -48.5316897),
    ("Password1234$", "Denice", "Wilsher", "dwilsher2o@addtoany.com", True, 14.4711923, 121.0206914),
    ("Password1234$", "Francesco", "Basham", "fbasham2p@joomla.org", True, 33.723039, -84.3436881),
    ("Password1234$", "Adolph", "Sebborn", "asebborn2q@independent.co.uk", True, 21.744605, 111.6180705),
    ("Password1234$", "Felice", "Odgers", "fodgers2r@salon.com", True, 24.1477358, 120.6736482),
]


def seed_users():
    for item in seed:
        x = User({
            "password": item[0],
            "first_name": item[1],
            "last_name": item[2],
            "email": item[3],
            "share_location": item[4],
            "coord_lat": item[5],
            "coord_long": item[6],
        })
        db.session.add(x)
        db.session.commit()


def seed_undo_users():
    db.session.execute('DELETE FROM users;')
    db.session.execute('ALTER SEQUENCE users_id_seq RESTART WITH 1;')
    db.session.commit()
