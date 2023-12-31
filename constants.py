
#directorios y urls
WEBDRIVER_ROOT_PATH = 'webdrivers/'
COOKIES_PATH = WEBDRIVER_ROOT_PATH+'galletas/'
CHROME_USER_DATA = WEBDRIVER_ROOT_PATH+'chromedata/User data'
PROFILE_PATH = f'{CHROME_USER_DATA}/Default'
EXTENSIONS_PATH = f'{PROFILE_PATH}/Extensions'
URBAN_VPN_EXT_ID = 'eppiocemhmnlbhjplcgkofciiegomcon'
URBAN_VPN_EXT_VERSION = '4.6.1_0'
URBAN_VPN_EXT_PATH = f'{EXTENSIONS_PATH}/{URBAN_VPN_EXT_ID}/{URBAN_VPN_EXT_VERSION}'
URBAN_VPN_LINK = f'chrome-extension://{URBAN_VPN_EXT_ID}/popup/index.html'
IG_URL = 'https://www.instagram.com'
IG_REGISTRATION_URL = IG_URL+'/accounts/emailsignup/'
IG_EXPLORE_TAG = IG_URL+'/explore/tags/'

#tiempo de espera maximo
WAIT_MAX = 60

#mensajes
LOGIN_INCORRECT_PWD_MSG = 'Tu contraseña no es correcta'

#xpaths para la pagina de inicio de sesion
USER_INPUT_XPATH = '//*[@id="loginForm"]/div/div[1]/div/label/input'
PWD_INPUT_XPATH = '//*[@id="loginForm"]/div/div[2]/div/label/input'
LOGIN_BUTTON_XPATH = '//*[@id="loginForm"]/div/div[3]/button'
LOGIN_ERROR_MSG_XPATH = '//*[@id="loginForm"]/span/div'

#xpaths para la pagina de registro
EMAIL_INPUT_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div[4]/div/label/input'
FULLNAME_INPUT_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div[5]/div/label/input'
REGUSERNAME_INPUT_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div[6]/div/label/input'
REGPWD_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div[7]/div/label/input'

#xpaths para la las ventanas emergentes de aceptar notificaciones y cookies de sesion
SAVE_SCOOKIES_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/section/div/button'
DONT_SAVE_SCOOKIES_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/div'
#NO_IG_NOTIFICATIONS_XPATH = '/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]'
#IG_NOTIFICATIONS_XPATH = '/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[1]'

#css selectors para los botones de la ventana emergente para aceptar notificaciones
ACCEPT_NOTIFICATIONS_SL = 'button._a9--._ap36._a9_0'
DONT_ACCEPT_NOTIFICATIONS_SL = 'button._a9--._ap36._a9_1'

#xpaths para el boton de busqueda
SEARCH_BUTTON_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/span/div/a'
SEARCH_INPUT_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div[1]/nav/div/header/div/div/div[1]/div/div/div/div/div/input'

#xpaths para la matriz de posts que aparecen al buscar un hashtag
#POSTS_MATRIX_XPATH = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/article/div/div/div'
#POST_LIKES_XPATH = '/html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/span/a'
#POST_LIKES_NUM_XPATH = '/html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/span/a/span/span'
#POST_LIKES_LIST = '/html/body/div[8]/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div'

#POST_LIKE_ACCOUNT = '/div/div/div/div[2]/div/div/div/a/div/span/div'
#POST_LIKE_FOLLOW_BT = '/div/div/div/div[3]/div/button'
SEARCH_BUTTON_SL = '#mount_0_0_mG > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1.x1dr59a3.xixxii4.x13vifvy.xeq5yr9.x1n327nk > div > div > div > div > div.x1iyjqo2.xh8yej3 > div:nth-child(2) > span > div > a'
SEARCH_BUTTON_CLASSES = 'x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd'
#SEARCH_BUTTON_SL = 'a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz._a6hd'
#SEARCH_INPUT_SL = '#mount_0_0_mi > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1.x1dr59a3.xixxii4.x13vifvy.xeq5yr9.x1n327nk > div > div > div.x10l6tqk.x1u3tz30.x1ja2u2z > div > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.x1plvlek.xryxfnj.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1d52u69.xktsk01.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div > div > input'
SEARCH_INPUT_SL = '#mount_0_0_TK > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x17snn68.x6osk4m.x1porb0y > section > div:nth-child(2) > nav > div > header > div > div > div.xq8finb > div > div > div > div > div > input'
ACCOUNTS_LIST='#mount_0_0_06>div>div>div.x9f619.x1n2onr6.x1ja2u2z>div>div>div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4>div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib>div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1.x1dr59a3.xixxii4.x13vifvy.xeq5yr9.x1n327nk>div>div>div.x10l6tqk.x1u3tz30.x1ja2u2z>div>div>div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.x1plvlek.xryxfnj.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1>div>div>div.x6s0dn4.x78zum5.xdt5ytf.x5yr21d.x1odjw0f.x1n2onr6.xh8yej3>div'
NOT_FOUND_MSG = 'No se han encontrado resultados.'
PAGE_NOT_FOUND_MSG = 'Página no encontrada'

POST_MATRIX_SL = '#mount_0_0_XB>div>div>div.x9f619.x1n2onr6.x1ja2u2z>div>div>div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4>div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib>div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x17snn68.x6osk4m.x1porb0y>section>main>article>div>div>div'
POST_OWNER_ACCOUNT_SL = 'body>div.x1n2onr6.xzkaem6>div.x9f619.x1n2onr6.x1ja2u2z>div>div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj>div>div>div>div>div.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe.x1qjc9v5.xjbqb8w.x1lcm9me.x1yr5g0i.xrt01vj.x10y3i5r.xr1yuqi.xkrivgy.x4ii5y1.x1gryazu.x15h9jz8.x47corl.xh8yej3.xir0mxb.x1juhsu6>div>article>div>div._ae6>div>div>div._aasi>div>header>div._aaqy._aaqz>div._aar0._ad95._aar1>div.x78zum5>div>div>span>span>div>a'
POST_ACCOUNT_LINK_CLASSES = 'x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz  _acan _acao _acat _acaw _aj1- _ap30 _a6hd'
#mount_0_0_xK > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x17snn68.x6osk4m.x1porb0y > div:nth-child(2) > section > main > div > header > section > ul
AC_FOLLOWERS_LINK_CLASSES = 'xl565be x1m39q7l x1uw6ca5 x2pgyrj'
AC_INFO_SECTION_CLASSES = 'x78zum5 x1q0g3np xieb3on'
AC_FOLLOWERS_SEC_CLASS = '_aano'
AC_FOLLOWER_CLASSES = 'x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3'

SEARCH_CANDIDATE_CLASSES = 'x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3'
#ACCOUNT_BOX_CLASSES = 'x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3'

ADD_EXTENSION_BUTTON_CLASSES = 'UywwFc-LgbsSe UywwFc-LgbsSe-OWXEXe-dgl2Hf'
LOCATION_ITEM_CLASS = 'locations__item'
SELECTION_INPUT_CLASSES = 'select-location__box select-location__box--search'
SELECTION_BOX_CLASSES ='select-location__box select-location__box--locations select-location__box--locations-visible'
AC_FOLLOWER_NAME_CLASSES = '_ap3a _aaco _aacw _aacx _aad7 _aade'
AC_FOLLOWER_FOLLOW_BT_CLASSES = ' _acan _acap _acas _aj1- _ap30'