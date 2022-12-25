function goToQuestion(qid, location){
	sessionStorage.setItem('scroll', `${location}$${document.documentElement.scrollTop}`)
	window.location.href = `${window.location.origin}/detail-question/${qid}/recent`;
}