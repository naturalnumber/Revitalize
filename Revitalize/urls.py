from django.urls import include, path
from rest_framework import routers

from Revitalize.views import ProfileViewSet, StringGroupViewSet, StringViewSet, TextViewSet, FormViewSet, SurveyViewSet, \
    QuestionViewSet, TextQuestionViewSet, IntRangeQuestionViewSet, SubmissionViewSet, TextResponseViewSet, \
    IntRangeResponseViewSet, TextElementViewSet, QuestionGroupViewSet, IntQuestionViewSet, FloatQuestionViewSet, \
    ExclusiveChoiceQuestionViewSet, MultiChoiceQuestionViewSet, IntResponseViewSet, FloatResponseViewSet, \
    ExclusiveChoiceResponseViewSet, MultiChoiceResponseViewSet

router = routers.DefaultRouter()

router.register('text', TextViewSet)
router.register('strings', StringViewSet)
router.register('string_groups', StringGroupViewSet)
router.register('profiles', ProfileViewSet)
router.register('forms', FormViewSet)
router.register('surveys', SurveyViewSet)
router.register('text_elements', TextElementViewSet)
router.register('question_groups', QuestionGroupViewSet)
router.register('questions', QuestionViewSet)
router.register('question_groups_text', TextQuestionViewSet)
router.register('question_groups_text', IntQuestionViewSet)
router.register('question_groups_text', FloatQuestionViewSet)
router.register('question_groups_int_range', IntRangeQuestionViewSet)
router.register('question_groups_int_range', ExclusiveChoiceQuestionViewSet)
router.register('question_groups_int_range', MultiChoiceQuestionViewSet)
router.register('submissions', SubmissionViewSet)
router.register('responses_text', TextResponseViewSet)
router.register('responses_text', IntResponseViewSet)
router.register('responses_text', FloatResponseViewSet)
router.register('responses_int_range', IntRangeResponseViewSet)
router.register('responses_int_range', ExclusiveChoiceResponseViewSet)
router.register('responses_int_range', MultiChoiceResponseViewSet)

urlpatterns = [
        path('', include(router.urls)),
]
