var naver_id_login = new naver_id_login("iTanYcwIz0n5CqfvCNb3", "http://127.0.0.1:8000/auth/naver/callback/");
var state = naver_id_login.getUniqState();
naver_id_login.setButton("white", 2,40);
naver_id_login.setDomain("http://127.0.0.1:8000");
naver_id_login.setState(state);
naver_id_login.setPopup();
naver_id_login.init_naver_id_login();