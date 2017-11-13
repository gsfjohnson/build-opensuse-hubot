%define name hubot
%define version 3.0.1
%define release 1
%define buildroot %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Name: %{name}
Version: %{version}
Release: %{release}
Summary: hubot

Group: Installation Script
License: MIT
Source: https://github.com/hubotio/hubot/archive/v%{version}.tar.gz
BuildRoot: %{buildroot}
Requires: nodejs
BuildRequires: nodejs
AutoReqProv: no

%description
A simple helpful robot for your Company

%prep
%setup -q -c -n %{name}

%build
npm prune --production
npm rebuild

%pre
getent group hubot >/dev/null || groupadd -r hubot
getent passwd hubot >/dev/null || useradd -r -g hubot -G hubot -d / -s /sbin/nologin -c "hubot" hubot

%install
mkdir -p %{buildroot}/usr/lib/hubot
cp -r ./ %{buildroot}/usr/lib/hubot
mkdir -p %{buildroot}/var/log/hubot

%post
systemctl enable /usr/lib/hubot/hubot.service

%clean
rm -rf %{buildroot}

%files
%defattr(644, hubot, hubot, 755)
/usr/lib/hubot
/var/log/hubot
