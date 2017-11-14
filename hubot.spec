%define realname hubot
%define pkg_name nodejs-hubot
%define version 3.0.1
%define release 1
%define buildroot %(mktemp -ud %{_tmppath}/%{realname}-%{version}-%{release}-XXXXXX)

Name: %{pkg_name}
Version: %{version}
Release: %{release}
Summary: hubot

Group: Installation Script
License: MIT
Source: %{realname}-%{version}.tar.bz2
Source100: hubot.initd
BuildRoot: %{buildroot}
Requires: nodejs
%{?el6:Requires: npm}
BuildRequires: nodejs
%{?el6:BuildRequires: npm}
AutoReqProv: no

%description
A simple helpful robot for your Company

%prep
%setup -q -c -n %{realname}-%{version}

%build
npm prune --production
npm rebuild

%pre
getent group hubot >/dev/null || groupadd -r hubot
getent passwd hubot >/dev/null || useradd -r -g hubot -G hubot -d / -s /sbin/nologin -c "hubot" hubot

%install
mkdir -p %{buildroot}/usr/lib/hubot
cp -rv %{realname}-%{version}/ %{buildroot}/usr/lib/hubot
mkdir -p %{buildroot}/var/log/hubot

%if 0%{?el6}
install -D -m 755 %{SOURCE100} $RPM_BUILD_ROOT/%{_initddir}/hubot
%endif

%if 0%{?el7}
%post
systemctl enable /usr/lib/hubot/hubot.service
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(644, hubot, hubot, 755)
/usr/lib/hubot
/var/log/hubot
%if 0%{?el6}
/%{_initddir}/hubot
%endif
