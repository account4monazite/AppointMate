     let currentCard = 0;  
        let totalCards = 10; 
        let isPlaying = true;
        let timer;            

        const carousel = document.getElementById('carousel');
        const dots = document.querySelectorAll('.dot');
        const pauseButton = document.querySelector('.controls .btn:nth-child(2)');

        function moveCarousel() {
            const moveDistance = currentCard * 320;
            
            carousel.style.transform = `translateX(-${moveDistance}px)`;
            
            updateDots();
        }

        function updateDots() {

            dots.forEach(dot => dot.classList.remove('active'));
            
            dots[currentCard].classList.add('active');
            
        }

        function nextCard() {
            currentCard++;
            
            if (currentCard >= totalCards) {
                currentCard = 0;
            }
            
            moveCarousel();
        }

        function previousCard() {
            currentCard--;
            
            if (currentCard < 0) {
                currentCard = totalCards - 1;
            }
            
            moveCarousel();
        }

        function goToCard(cardNumber) {
            currentCard = cardNumber;
            moveCarousel();
        }

        function startAutoPlay() {
            timer = setInterval(nextCard, 3000); 
        }

        function stopAutoPlay() {
            clearInterval(timer);
        }

        function toggleAutoPlay() {
            if (isPlaying) {
                stopAutoPlay();
                pauseButton.textContent = 'Play';
                isPlaying = false;
            } else {
                startAutoPlay();
                pauseButton.textContent = 'Pause';
                isPlaying = true;
            }
        }

        const allCards = document.querySelectorAll('.cards');
        
        allCards.forEach(function(card, index) {
            card.addEventListener('mouseenter', function() {
                console.log('Hovered over card', index); 
                stopAutoPlay();
            });

            card.addEventListener('mouseleave', function() {
                console.log('Left card', index); 
                if (isPlaying) {
                    startAutoPlay();
                }
            });
        });

        startAutoPlay();