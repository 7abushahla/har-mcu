"""Model builders for HAR experiments."""

from src.models.deepconv_lstm import (  # noqa: F401
    build_deepconv_lstm,
    build_deepconv_lstm_conv2d,
    compile_deepconv_lstm,
)
from src.models.daghero_cnn_searchspace_tf import (  # noqa: F401
    build_daghero_2layer,
    build_daghero_4layer,
    build_daghero_cnn_template,
    compile_daghero_cnn,
)
from src.models.repmobile_folded_tf import (  # noqa: F401
    build_repmobile_folded,
    compile_repmobile_folded,
)
from src.models.tcn_attention_har_tf import (  # noqa: F401
    build_tahar_student_cnn,
    build_tahar_student_gru,
    build_tahar_student_lstm,
    build_tcn_attention_har_teacher,
    compile_tcn_attention,
)
from src.models.tcn_inception_tf import (  # noqa: F401
    build_tcn_inception,
    compile_tcn_inception,
)
from src.models.xtinyhar_student_tf import (  # noqa: F401
    build_xtinyhar_student,
    compile_xtinyhar_student,
)
