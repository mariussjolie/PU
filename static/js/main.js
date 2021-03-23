
class TypeWriter {
    constructor(txtElement, words, wait = 3000) {
      this.txtElement = txtElement;
      this.words = words;
      this.txt = '';
      this.wordIndex = 0;
      this.wait = parseInt(wait, 10);
      this.type();
      this.isDeleting = false;
    }
  
    type() {
      const current = this.wordIndex % this.words.length;
      const fullTxt = this.words[current];

      if(this.isDeleting) {
        this.txt = fullTxt.substring(0, this.txt.length - 1);
      } else {
        this.txt = fullTxt.substring(0, this.txt.length + 1);
      }
  
      this.txtElement.innerHTML = `<span class="txt">${this.txt}</span>`;
  
      let typeSpeed = 250;
  
      if(this.isDeleting) {
        typeSpeed /= 2;
      }
  
      if(!this.isDeleting && this.txt === fullTxt) {
        typeSpeed = this.wait;
        this.isDeleting = true;
      } else if(this.isDeleting && this.txt === '') {
        this.isDeleting = false;
        this.wordIndex++;
        typeSpeed = 500;
      }
  
      setTimeout(() => this.type(), typeSpeed);
    }
  }
  
  document.addEventListener('DOMContentLoaded', init);
  
  function init() {
    const txtElement = document.querySelector('.txt-type');
    const words = JSON.parse(txtElement.getAttribute('data-words'));
    const wait = txtElement.getAttribute('data-wait');
    new TypeWriter(txtElement, words, wait);
  }

  function addComment() {
    var x = document.createElement("P")
    var y = document.getElementById("commentarea")
    var i = y.value
    x.style.cssText ="position: float; display: block; text-content: center; border: 5px solid white; padding: 30px"
    x.append(i)
    document.getElementById("commentsection").append(x)
  }
