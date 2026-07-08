document.addEventListener('DOMContentLoaded', function () {
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');

  if (loginForm) {
    loginForm.addEventListener('submit', function (event) {
      const password = document.getElementById('id_password');

      if (password.value.length < 1) {
        event.preventDefault();
        showAlert('رمز عبور باید حداقل ۴ کاراکتر باشد.', 'error');
      } else {
        hideAlert();
      }
    });
  }

  if (registerForm) {
    registerForm.addEventListener('submit', function (event) {
      const username = document.getElementById('id_username');
      const password = document.getElementById('id_password');
      const passwordConfirm = document.getElementById('id_password_confirm');

      let message = '';
      if (username.value.trim().length < 3) {
        message = 'نام کاربری باید حداقل ۳ کاراکتر باشد.';
      } else if (password.value.length < 4) {
        message = 'رمز عبور باید حداقل ۴ کاراکتر باشد.';
      } else if (password.value !== passwordConfirm.value) {
        message = 'تکرار رمز عبور با رمز عبور مطابقت ندارد.';
      }

      if (message) {
        event.preventDefault();
        showAlert(message, 'error');
      } else {
        hideAlert();
      }
    });
  }
});