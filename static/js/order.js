function toman(amount) {
  return amount.toLocaleString('fa-IR') + ' تومان';
}

document.addEventListener('DOMContentLoaded', function () {
  const typeOptions = document.querySelectorAll('.type-opt');
  const typeRadios = document.querySelectorAll('input[name="order_type"]');
  const calcButton = document.getElementById('calc-btn');
  const recalcButton = document.getElementById('recalc-btn');
  const estimateSlot = document.getElementById('estimate-slot');

  // ظاهر انتخاب‌شده با CSS و :has(input:checked) کنترل می‌شود؛
  // این بخش فقط برای مرورگرهای قدیمی‌تر بدون پشتیبانی از :has() است.
  typeRadios.forEach(function (radio) {
    radio.addEventListener('change', function () {
      typeOptions.forEach(function (o) { o.classList.remove('selected'); });
      radio.closest('.type-opt').classList.add('selected');
    });
  });

  // نمایش اسم فایل انتخاب‌شده برای پیوست سفارش
  const fileInput = document.getElementById('id_attachment');
  const fileField = document.getElementById('file-field');
  const fileFieldText = document.getElementById('file-field-text');
  if (fileInput) {
    fileInput.addEventListener('change', function () {
      if (fileInput.files.length > 0) {
        fileFieldText.textContent = fileInput.files[0].name;
        fileField.classList.add('has-file');
      } else {
        fileFieldText.textContent = 'فایلی انتخاب نشده — برای انتخاب کلیک کنید';
        fileField.classList.remove('has-file');
      }
    });
  }

  calcButton.addEventListener('click', function () {
    const pages = document.getElementById('id_pages').value;
    const language = document.getElementById('id_language').value;
    const format = document.getElementById('id_format').value;
    const type = document.querySelector('input[name="order_type"]:checked').value;

    if (!pages || Number(pages) < 1) {
      showToast('تعداد صفحات را درست وارد کنید.');
      return;
    }

    calcButton.disabled = true;
    calcButton.textContent = 'در حال محاسبه...';

    const params = new URLSearchParams({ order_type: type, pages, language, format });
    const estimateUrl = calcButton.dataset.estimateUrl + '?' + params.toString();

    fetch(estimateUrl)
      .then(function (response) { return response.json(); })
      .then(function (data) {
        if (!data.ok) {
          showAlert(data.error || 'محاسبه‌ی قیمت با خطا مواجه شد.', 'error');
          return;
        }
        document.getElementById('est-price').textContent = toman(data.price);
        document.getElementById('est-days').textContent = data.days + ' روز کاری';
        document.getElementById('est-half').textContent = toman(data.half_payment);
        estimateSlot.hidden = false;
      })
      .catch(function () {
        showAlert('ارتباط با سرور برقرار نشد. دوباره تلاش کنید.', 'error');
      })
      .finally(function () {
        calcButton.disabled = false;
        calcButton.textContent = 'محاسبه هزینه و زمان تخمینی';
      });
  });

  if (recalcButton) {
    recalcButton.addEventListener('click', function () {
      estimateSlot.hidden = true;
    });
  }
});