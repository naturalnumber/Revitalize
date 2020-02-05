from django.urls import include, path
from rest_framework import routers

from Revitalize.views import BooleanChoiceQuestionViewSet, BooleanChoiceResponseViewSet, ExclusiveChoiceQuestionViewSet, \
    ExclusiveChoiceResponseViewSet, FloatQuestionViewSet, FloatRangeQuestionViewSet, FloatRangeResponseViewSet, \
    FloatResponseViewSet, FormViewSet, IntQuestionViewSet, IntRangeQuestionViewSet, IntRangeResponseViewSet, \
    IntResponseViewSet, MultiChoiceQuestionViewSet, MultiChoiceResponseViewSet, ProfileViewSet, QuestionGroupViewSet, \
    QuestionViewSet, StringGroupViewSet, StringViewSet, SubmissionViewSet, SurveyViewSet, TextElementViewSet, \
    TextQuestionViewSet, TextResponseViewSet, TextViewSet

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
router.register('question_text', TextQuestionViewSet)
router.register('question_int', IntQuestionViewSet)
router.register('question_float', FloatQuestionViewSet)
router.register('question_int_range', IntRangeQuestionViewSet)
router.register('question_float_range', FloatRangeQuestionViewSet)
router.register('question_boolean_choice', BooleanChoiceQuestionViewSet)
router.register('question_exclusive_choice', ExclusiveChoiceQuestionViewSet)
router.register('question_multi_choice', MultiChoiceQuestionViewSet)
router.register('submissions', SubmissionViewSet)
router.register('responses_text', TextResponseViewSet)
router.register('responses_int', IntResponseViewSet)
router.register('responses_float', FloatResponseViewSet)
router.register('responses_int_range', IntRangeResponseViewSet)
router.register('responses_float_range', FloatRangeResponseViewSet)
router.register('responses_boolean_choice', BooleanChoiceResponseViewSet)
router.register('responses_exclusive_choice', ExclusiveChoiceResponseViewSet)
router.register('responses_multi_choice', MultiChoiceResponseViewSet)

urlpatterns = [
        path('', include(router.urls)),
]
