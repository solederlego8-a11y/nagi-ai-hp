// NAGI AI - 共通スクリプト（ナビ開閉 / FAQアコーディオン）
document.addEventListener("DOMContentLoaded", function () {
  // モバイルナビ開閉
  var navToggle = document.querySelector(".nav-toggle");
  if (navToggle) {
    navToggle.addEventListener("click", function () {
      document.body.classList.toggle("nav-open");
    });
  }

  // FAQアコーディオン
  document.querySelectorAll(".faq-item").forEach(function (item) {
    var q = item.querySelector(".faq-q");
    if (!q) return;
    q.addEventListener("click", function () {
      var wasOpen = item.classList.contains("is-open");
      document.querySelectorAll(".faq-item.is-open").forEach(function (other) {
        if (other !== item) other.classList.remove("is-open");
      });
      item.classList.toggle("is-open", !wasOpen);
    });
  });

  // 問い合わせフォームは https://formsubmit.co/naoren.38@gmail.com へ通常のPOST送信する
  // （JSでのpreventDefaultは行わない。送信後は_nextで指定したcontact-thanks.htmlへ遷移する）
});
