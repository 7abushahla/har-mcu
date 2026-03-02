"""Model builders for HAR experiments."""

from src.models.deepconv_lstm import (  # noqa: F401
    build_deepconv_lstm,
    build_deepconv_lstm_conv2d,
    compile_deepconv_lstm,
)
from src.models.daghero_cnn_searchspace_tf import (  # noqa: F401
    build_daghero_2layer,
    build_daghero_2layer_conv2d,
    build_daghero_4layer,
    build_daghero_4layer_conv2d,
    build_daghero_cnn_template,
    build_daghero_cnn_template_conv2d,
    compile_daghero_cnn,
)
from src.models.repmobile_folded_tf import (  # noqa: F401
    build_repmobile_folded,
    build_repmobile_folded_conv2d,
    compile_repmobile_folded,
)
from src.models.serialization import load_checkpoint_model  # noqa: F401
from src.models.tcn_attention_har_tf import (  # noqa: F401
    build_tahar_student_cnn,
    build_tahar_student_gru,
    build_tahar_student_lstm,
    build_tcn_attention_har_teacher,
    build_tcn_attention_har_teacher_conv2d,
    compile_tcn_attention,
)
from src.models.tcn_inception_tf import (  # noqa: F401
    build_tcn_inception,
    build_tcn_inception_conv2d,
    compile_tcn_inception,
)
from src.models.xtinyhar_student_tf import (  # noqa: F401
    build_xtinyhar_student,
    build_xtinyhar_student_conv2d,
    compile_xtinyhar_student,
)
