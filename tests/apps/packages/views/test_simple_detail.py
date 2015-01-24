import pytest

from django.core.urlresolvers import reverse

from localshop.apps.permissions.models import CIDR
from tests.apps.packages.factories import ReleaseFileFactory


@pytest.mark.django_db
def test_success(client, admin_user, pypi_stub):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)
    release_file = ReleaseFileFactory()

    response = client.get(reverse('packages-simple:simple_detail', kwargs={
        'slug': release_file.release.package.name,
        'version': '',
    }))

    assert response.status_code == 200
    assert 'Links for test-package' in response.content
    assert ('<a href="/packages/test-package/download/1/test-1.0.0-sdist.zip'
            '#md5=62ecd3ee980023db87945470aa2b347b" rel="package">'
            'test-1.0.0-sdist.zip</a>') in response.content


@pytest.mark.django_db
def test_missing_package(client, admin_user, pypi_stub):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)

    response = client.get(reverse('packages-simple:simple_detail', kwargs={
        'slug': 'minibar',
        'version': '',
    }))

    assert response.status_code == 200
    assert 'Links for minibar' in response.content
    assert '<a href="/packages/minibar/download/1/minibar-0.4.0-py2.py3-none-any.whl#md5=9eac01120a372609e0afa3b236d9ed2d" rel="package">minibar-0.4.0-py2.py3-none-any.whl</a>' in response.content
    assert '<a href="/packages/minibar/download/2/minibar-0.4.0.tar.gz#md5=9eac01120a372609e0afa3b236d9ed2d" rel="package">minibar-0.4.0.tar.gz</a>' in response.content
    assert '<a href="/packages/minibar/download/3/minibar-0.1-py2.py3-none-any.whl#md5=cb5ae17636e975f9bf71ddf5bc542075" rel="package">minibar-0.1-py2.py3-none-any.whl</a>' in response.content
    assert '<a href="/packages/minibar/download/4/minibar-0.1.tar.gz#md5=cb5ae17636e975f9bf71ddf5bc542075" rel="package">minibar-0.1.tar.gz</a>' in response.content