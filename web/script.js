const api = "http://newsapi.org/v2/everything?q=health&apiKey=cd0b9c1adc62482683bf628e3993dd34";
const a1Title = document.querySelector(".a1Title");
const a2Title = document.querySelector(".a2Title");
const a3Title = document.querySelector(".a3Title");

const article1 = document.querySelector("#article1");
const article2 = document.querySelector("#article2");
const article3 = document.querySelector("#article3");

fetch(api)
    .then(response => {
        return response.json();
    })
    .then(data => {
        console.log(data);

        const title1 = data.articles[0].title;
        const image1 = data.articles[0].urlToImage;
        const url1 = data.articles[0].url;
        a1Title.textContent = title1;
        article1.style.backgroundImage = `url(${image1})`;
        article1.href = url1;

        const title2 = data.articles[1].title;
        const image2 = data.articles[1].urlToImage;
        const url2 = data.articles[1].url;
        a2Title.textContent = title2;
        article2.style.backgroundImage = `url(${image2})`;
        article2.href = url2;

        const title3 = data.articles[2].title;
        const image3 = data.articles[2].urlToImage;
        const url3 = data.articles[2].url;
        a3Title.textContent = title3;
        article3.style.backgroundImage = `url(${image3})`;
        article3.href = url3;
    });