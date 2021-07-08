from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from review.models import *
import re


def add_review(request, doc_id):
    doctor = get_object_or_404(Doctor, pk=doc_id)
    spec_str = ', '.join(doctor.specialty.all())

    if request.method != 'POST':
        return render(request, 'review/add_review.html', {'doctor': doctor, 'specialty': spec_str})

    review_text = request.POST['review_text']

    new_review = Review()
    new_review.review_doctor = doctor
    new_review.original_rev_text = review_text
    new_review.processed_rev_text = new_review.remake_rev()
    new_review.ip_address = '127.0.0.1'
    if request.user.is_authenticated:
        new_review.user = request.user
    new_review.save()

    return HttpResponse('<h1>Отзыв добавлен</h1>')


def review(request):
    if not request.user.is_staff:
        raise Http404

    reviews = Review.objects.select_related('review_doctor', 'user').order_by('review_date')
    list_curse = [s.word for s in CurseWord.objects.all()]
    list_ex_words = [s.word for s in ExceptionWord.objects.all()]

    for rev in reviews:
        text = rev.processed_rev_text.split(' ')
        words_list = []
        for word in text:
            for c_word in list_curse:
                if re.search(c_word, word) is not None and word not in list_ex_words:
                    sym = ''
                    if word[-1] in ['.', ',', '!', '?', ';', ':']:
                        *word, sym = word
                    words_list.append(f'<span style="background-color: red; '
                                      f'color: white;">{"".join(word)}</span>{sym}')
                    word = ''
            words_list.append(word)
        rev.processed_rev_text = ' '.join(words_list)

    return render(request, 'review/reviews.html', {'reviews': reviews})
