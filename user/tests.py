from django.test import TestCase

# Create your tests here.

# <div class="id_wrap">
#                 {% if error_msg %}
#                     <p style="color:red">{{ error_msg }}</p>
#                 {% endif %}
#                 <div class="id_input_box">
#                     <label>아이디</label>
#                     <span class="input-style">
#                         <input type="text" name="username" placeholder="아이디를 입력하세요" required/>
#                     </span>
#                 </div>
#             </div>
#             <div class="pw_wrap">
#                 <div class="pw_input_box">
#                     <label>비밀번호</label>
#                     <input type="password" name="password" placeholder="비밀번호를 입력하세요" maxlength="12" minlength="8" required/>
#                 </div>
#             </div>