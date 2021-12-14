import pytest

from sentinels.models import Sentinel


@pytest.fixture
def a_highlighter(django_user_model):
    return django_user_model.objects.create(
        username="userjohn", password="qwer1234qwer1234"
    )


@pytest.fixture
def a_sentinel():
    return Sentinel.objects.create(
        title="A sample title",
        description="""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas semper tristique ipsum. Pellentesque ut hendrerit orci, at sagittis nisl. Suspendisse in sodales tortor, vel malesuada nisi. Vestibulum ultricies porta tellus, egestas convallis orci vehicula euismod. Fusce egestas in mauris vel finibus. Donec sed quam rutrum, varius dui sed, interdum odio. Suspendisse feugiat venenatis neque, eu sagittis lectus congue eu.

            Suspendisse sit amet libero non purus porttitor mattis. Praesent vehicula enim purus, sed mollis nisi ornare sit amet. Phasellus maximus, elit eu pretium imperdiet, justo sapien viverra nisl, ac malesuada dolor nunc eu quam. Sed congue nibh mauris, sit amet consectetur risus tempus in. In commodo, risus eget consectetur molestie, velit metus congue metus, ut tristique neque tellus eget purus. In eget placerat nisl, a elementum enim. Quisque lobortis mi eget mollis interdum. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam erat volutpat. Interdum et malesuada fames ac ante ipsum primis in faucibus. Pellentesque nisl justo, consequat eu dolor ut, molestie tincidunt quam. Mauris tincidunt quis magna nec convallis. Nulla pretium leo id tincidunt auctor. Nunc mi eros, condimentum ut interdum ac, consectetur ac risus. Fusce egestas dictum arcu non iaculis.

            Duis eleifend tempor ullamcorper. Curabitur placerat sapien eget purus vulputate, id imperdiet diam accumsan. Nam iaculis tellus magna. Nulla nisi massa, semper ac iaculis in, varius eu dui. Quisque luctus felis augue, at porttitor felis vestibulum eget. Nullam nec erat viverra, facilisis quam efficitur, elementum sem. Pellentesque faucibus sagittis augue, a elementum urna placerat quis. Morbi congue risus at cursus blandit. Aliquam erat volutpat.

            Ut vitae metus in risus interdum convallis. Vivamus finibus diam non aliquet suscipit. Mauris molestie imperdiet elit, eget egestas augue condimentum eu. Nullam varius in purus in facilisis. Fusce vehicula varius metus sed bibendum. Sed a dolor massa. Aliquam vel molestie nisi. Nam finibus, nisl ac eleifend maximus, augue purus interdum ipsum, sed vestibulum urna dui sed tellus. Donec ullamcorper, metus at mollis fermentum, mi risus mollis ipsum, vel dictum turpis purus sed nibh.

            Donec consequat at ligula id accumsan. Curabitur nec varius leo. Morbi vel elit id felis scelerisque laoreet. Praesent id arcu sit amet magna elementum bibendum non sit amet urna. Nam id nunc sodales, varius nisl et, fringilla libero. Etiam pharetra nisl odio, ac lacinia quam porttitor vitae. Curabitur at scelerisque nulla, vitae ultricies augue. Donec non laoreet neque. Nam ut libero ut dui porta lobortis. Vivamus et finibus ante. Integer vitae nunc a quam vulputate mattis. Aliquam eu risus at nisi congue fringilla sit amet at tortor. Nulla elementum tortor in arcu sodales, ut tristique lorem vestibulum. Vivamus posuere elementum nunc et eleifend. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae;
        """,
    )
